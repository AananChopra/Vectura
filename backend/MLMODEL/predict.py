import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import torch.nn as nn
import os
class LSTMCountryModel(nn.Module):
    def __init__(self, num_countries, embedding_dim=8, hidden_dim=64):
        super(LSTMCountryModel, self).__init__()
        self.embedding = nn.Embedding(num_countries, embedding_dim)
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim + embedding_dim, 1)

    def forward(self, country_ids, sequences):
        country_embed = self.embedding(country_ids)
        lstm_out, _ = self.lstm(sequences)
        last_output = lstm_out[:, -1, :]
        combined = torch.cat((last_output, country_embed), dim=1)
        return self.fc(combined)

def get_country_forecast(country: str, years_to_predict: int, model_path='model5.pt', data_path='privclean.csv', seq_len=10):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file '{data_path}' not found.")

    df = pd.read_csv(data_path)
    df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
    df.columns = df.columns.str.strip()
    df_long = df.melt(id_vars='country_name', var_name='year', value_name='value').dropna()
    df_long['year'] = df_long['year'].astype(int)
    df_long = df_long.sort_values(by=['country_name', 'year']).reset_index(drop=True)

    country_encoder = LabelEncoder()
    df_long['country_id'] = country_encoder.fit_transform(df_long['country_name'])

    if country not in country_encoder.classes_:
        raise ValueError(f"Country '{country}' not found in data.")

    country_id = country_encoder.transform([country])[0]
    country_df = df_long[df_long['country_name'] == country].sort_values('year')

    scaler = MinMaxScaler()
    scaler.fit(country_df[['value']])

    recent_values = country_df['value'].values[-seq_len:]
    if len(recent_values) < seq_len:
        raise ValueError(f"Not enough data for {country} (need {seq_len}, got {len(recent_values)}).")
    input_seq = scaler.transform(recent_values.reshape(-1, 1)).flatten().tolist()

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found.")

    model = torch.load(model_path, map_location=device)
    model.to(device)
    model.eval()

    future_preds = {}
    current_year = int(country_df['year'].max())

    for _ in range(years_to_predict):
        seq_tensor = torch.tensor(input_seq, dtype=torch.float).unsqueeze(0).unsqueeze(-1).to(device)
        country_tensor = torch.tensor([country_id], dtype=torch.long).to(device)

        with torch.no_grad():
            pred_scaled = model(country_tensor, seq_tensor).item()
            pred = scaler.inverse_transform([[pred_scaled]])[0][0]

        current_year += 1
        future_preds[current_year] = round(pred, 2)
        input_seq = input_seq[1:] + [pred_scaled]

    return future_preds

import matplotlib.pyplot as plt
import pandas as pd

def plot_predictions(full_country_df, predictions, history_years=20):
    country_name = full_country_df['country_name'].iloc[0]

    # Get last `history_years` of historical data
    historical = full_country_df[['year', 'value']].copy()
    historical = historical.sort_values('year')
    historical_tail = historical.tail(history_years)

    # Prepare forecast data
    future = pd.DataFrame({
        'year': list(predictions.keys()),
        'value': list(predictions.values())
    })

    # Combine both for consistent plotting
    combined = pd.concat([historical_tail, future], ignore_index=True)

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(historical_tail['year'], historical_tail['value'], label='Historical', marker='o', color='blue')
    plt.plot(future['year'], future['value'], label='Forecast', marker='x', color='orange', linestyle='--')

    # Optional: vertical line at transition
    plt.axvline(x=historical_tail['year'].max(), color='gray', linestyle=':', linewidth=1)

    plt.title(f"{country_name} - Last {history_years} Years and Forecast")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#example
predictions = get_country_forecast("Ghana", 10)
print(predictions)

