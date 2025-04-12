import os
import pandas as pd
import json
import google.generativeai as genai
from typing import Dict, List, Union

# Debugging setup
print("Current Working Directory:", os.getcwd())

# File path configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'MLMODEL', 'privclean.csv')

def load_dataframe() -> pd.DataFrame:
    """Load and return the financial data DataFrame."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Data file '{CSV_PATH}' not found.")
    df = pd.read_csv(CSV_PATH)
    # Clean column names by stripping whitespace
    df.columns = df.columns.str.strip()
    return df

# Initialize data
try:
    df = load_dataframe()
    country_list = df['country_name'].unique().tolist()  # Fixed column name (removed space)
    print(f"Loaded data with {len(country_list)} countries")
except Exception as e:
    print(f"Error loading data: {str(e)}")
    country_list = []
    df = pd.DataFrame()

# Gemini API configuration
genai.configure(api_key="AIzaSyASjCwVvZUCK6WdC03nQm-1pM8aSAy5WCo")
model = genai.GenerativeModel('gemini-1.5-flash')

def decide_risk(country: str, UBal: str, UOut: str, UInc: str, 
                year: int, yearpred: float, modelresult: Dict) -> Dict[str, Union[str, List[str]]]:
    """
    Generate a comprehensive risk assessment with structured output.
    
    Args:
        country: User's country of residence
        UBal: EMI/loan information
        UOut: Monthly expenses breakdown
        UInc: Monthly income
        year: Current year for analysis
        yearpred: Predicted debt percentage
        modelresult: Historical and forecast data
        
    Returns:
        Dictionary containing:
        - risk_level: Categorized risk
        - summary: Detailed analysis
        - recommendations: List of actionable suggestions
        - debt_ratio: Calculated debt-to-income ratio
    """
    prompt = f"""
    Financial Risk Assessment Request:
    
    Country: {country}
    Current Year: {year}
    National Debt Average: {yearpred}% of GDP
    
    User Financials:
    - Monthly Income: {UInc}
    - Monthly Expenses: {UOut}
    - Loan Details: {UBal}
    
    Historical/Predicted Data:
    {json.dumps(modelresult, indent=2)}
    
    Calculate:
    1. Debt-to-income ratio (format: +XX% or -XX%)
    2. Risk category based on:
        +30%+ = Very High Risk 🚨
        +15-29.99% = High Risk ⚠  
        -15% to +14.99% = Moderate Risk ⚖
        -15.01% to -30% = Low Risk ✅
        <-30% = Very Low Risk 🟢
    
    Return JSON format (NO additional text):
    {{
        "risk_level": "High Risk",
        "summary": "2-3 sentence analysis...",
        "recommendations": [
            "First recommendation...",
            "Second recommendation..."
        ],
        "debt_ratio": "+XX%"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        
        # Validate response structure
        required_keys = ['risk_level', 'summary', 'recommendations', 'debt_ratio']
        if not all(key in result for key in required_keys):
            raise ValueError("Missing required keys in AI response")
            
        return {
            'risk_level': result['risk_level'],
            'summary': result['summary'],
            'recommendations': result['recommendations'],
            'debt_ratio': result['debt_ratio'],
            'raw_ai_response': response.text  # For debugging
        }
        
    except json.JSONDecodeError:
        # Fallback to simple text response if JSON parsing fails
        return {
            'risk_level': "Unknown",
            'summary': response.text,
            'recommendations': [],
            'debt_ratio': "N/A",
            'raw_ai_response': response.text
        }
    except Exception as e:
        return {
            'error': str(e),
            'risk_level': "Error",
            'summary': "Could not generate analysis",
            'recommendations': [],
            'debt_ratio': "N/A"
        }

def decide_country(user_country: str) -> str:
    """
    Normalize country name input with AI assistance.
    
    Args:
        user_country: Raw country input from user
        
    Returns:
        Normalized country name matching our dataset
    """
    if not country_list:
        return user_country  # Fallback if no country data loaded
    
    prompt = f"""
    Strictly select ONLY from these countries (return raw value exactly as shown):
    {json.dumps(country_list, indent=2)}
    
    User input: "{user_country}"
    
    Return ONLY the matching country name from the list above.
    Do NOT include any other text, explanations, or formatting.
    """
    
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip()
        
        # Verify the response is in our country list
        if cleaned_response in country_list:
            return cleaned_response
        return user_country  # Fallback to original input
    except Exception:
        return user_country

# Example usage (for testing)
if __name__ == "__main__":
    test_country = decide_country("indian")
    print(f"Country normalized: {test_country}")
    
    test_analysis = decide_risk(
        country="India",
        UBal="One loan of ₹50,000, EMI over 12 months at 8% interest",
        UOut="Rent: ₹15,000, Food: ₹8,000, Utilities: ₹5,000",
        UInc="₹75,000",
        year=2024,
        yearpred=18.5,
        modelresult={"2023": 17.2, "2024": 18.5, "2025": 19.1}
    )
    print(json.dumps(test_analysis, indent=2))