from MLMODEL.prompts import decide_country, decide_risk
import torch
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import torch.nn as nn
import os
import pandas as pd
import numpy as np
import json
from typing import Dict

def get_country_forecast(
    country: str, 
    years_to_predict: int = 5,
    model_path: str = os.path.join(os.path.dirname(__file__), 'model5.pt'),
    data_path: str = os.path.join(os.path.dirname(__file__), 'privclean.csv'),
    seq_len: int = 10
) -> Dict[int, float]:
    """
    Generates economic forecasts for a given country using an LSTM model.
    
    Args:
        country: Name of the country to forecast
        years_to_predict: Number of future years to predict (default: 5)
        model_path: Path to the trained PyTorch model
        data_path: Path to the CSV data file
        seq_len: Length of input sequence for the model
    
    Returns:
        Dictionary with years as keys and predicted values as floats
    
    Raises:
        FileNotFoundError: If data or model files are missing
        ValueError: For invalid inputs or data issues
        RuntimeError: For model loading or prediction failures
    """
    # Validate inputs
    if not isinstance(country, str) or not country.strip():
        raise ValueError("Country name must be a non-empty string")
    if years_to_predict <= 0:
        raise ValueError("Years to predict must be positive")
    if seq_len <= 0:
        raise ValueError("Sequence length must be positive")

    # Data loading and validation
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")

    try:
        # Load and clean data
        df = pd.read_csv(data_path)
        
        # Fix: Proper column cleaning and validation
        df = df.drop(columns=[col for col in df.columns if 'Unnamed' in str(col)], errors='ignore')
        df.columns = df.columns.str.strip()
        
        # Validate required columns
        required_columns = ['country_name'] + [str(y) for y in range(2000, 2023)]  # Adjust years as needed
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Data file missing required columns: {missing_cols}")
    
        # Melt and clean data
        df_long = df.melt(id_vars='country_name', var_name='year', value_name='value').dropna()
        
        # Convert year to integer safely
        df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce')
        df_long = df_long.dropna(subset=['year'])
        df_long['year'] = df_long['year'].astype('int64')
        df_long = df_long.sort_values(by=['country_name', 'year']).reset_index(drop=True)

        # Country encoding with validation
        country_encoder = LabelEncoder()
        df_long['country_id'] = country_encoder.fit_transform(df_long['country_name'])
        
        if country not in country_encoder.classes_:
            available = list(country_encoder.classes_)
            raise ValueError(f"Country '{country}' not in dataset. Available: {available}")

        # Prepare input sequence
        country_df = df_long[df_long['country_name'] == country].sort_values('year')
        if len(country_df) == 0:
            raise ValueError(f"No data available for country: {country}")
        
        # Normalize values
        scaler = MinMaxScaler()
        try:
            scaler.fit(country_df[['value']])
        except ValueError as e:
            raise ValueError(f"Invalid value data: {str(e)}")
        
        recent_values = country_df['value'].values[-seq_len:]
        if len(recent_values) < seq_len:
            raise ValueError(f"Insufficient data for {country}. Need {seq_len} values, got {len(recent_values)}")

        input_seq = scaler.transform(recent_values.reshape(-1, 1)).flatten().tolist()
        country_id = country_encoder.transform([country])[0]

        # Load model with enhanced error handling
        try:
            model = load_model(model_path, num_countries=len(country_encoder.classes_))
            model.eval()
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {str(e)}")

        # Generate predictions
        future_preds = {}
        current_year = int(country_df['year'].max())
        
        with torch.no_grad():
            for _ in range(years_to_predict):
                try:
                    seq_tensor = torch.tensor(input_seq, dtype=torch.float32).unsqueeze(0).unsqueeze(-1)
                    country_tensor = torch.tensor([country_id], dtype=torch.long)
                    
                    pred_scaled = model(country_tensor, seq_tensor).item()
                    pred = scaler.inverse_transform([[pred_scaled]])[0][0]
                    
                    current_year += 1
                    future_preds[current_year] = round(pred, 2)
                    input_seq = input_seq[1:] + [pred_scaled]
                except Exception as e:
                    raise RuntimeError(f"Prediction failed for year {current_year + 1}: {str(e)}")

        return future_preds

    except pd.errors.EmptyDataError:
        raise ValueError("Data file is empty or corrupt")
    except Exception as e:
        raise RuntimeError(f"Forecast generation failed: {str(e)}")


def get_value_by_year(data: Dict[int, float], year: int = 2025) -> float:
    """
    Safely gets the forecast value for a specific year.
    
    Args:
        data: Dictionary of year-value pairs
        year: The year to look up
    
    Returns:
        The forecast value or 0.0 if not found
    """
    try:
        return float(data.get(year, 0.0))
    except (TypeError, ValueError):
        return 0.0