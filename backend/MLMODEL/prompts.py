import google.generativeai as genai
import pandas as pd

df = pd.read_csv('privclean.csv')
country_list = df['country_name '].unique().tolist()
genai.configure(api_key="AIzaSyASjCwVvZUCK6WdC03nQm-1pM8aSAy5WCo")
model = genai.GenerativeModel('gemini-1.5-flash')

def decide_risk(country,UBal,UOut,UInc,year,yearpred,modelresult):
    prompt = f"""
    If the Annual Average of Private Debt Loans and Debt Securities (Percent of GDP) value in year {year}, {country}, is {yearpred}

    A Person Living in {country} has following EMIs: {UBal}, Monthly Expenses: {UOut}, Monthly Income: {UInc},

    What Percentage is he over or under the country average, if he is over the average give the answer in +VE, if he is under give the Answer is Negative.

    Also Allot His Risk into the Following Categories: 
    Category	Deviation Range	Risk Level
    1. Very High Risk	+30% or more	🚨 Critical
    2. High Risk	+15% to +29.99%	⚠ Concerning
    3. Moderate Risk	-15% to +14.99%	⚖ Stable
    4. Low Risk	-15.01% to -30%	✅ Safe
    5. Very Low Risk	Lower than -30%	🟢 Very Stable"


    here some past and future predicted annual averages which might help your decision making: {modelresult}

    remove considerations and limitations, speak as if you are an agent who is trying to help a user who has given you this data
    """

    response = model.generate_content(prompt)
    return response.text.strip()

def decide_country(user_country):
    prompt = f"""
    The user has specified a country that is {user_country}, they might have made spelling or gramatical errors, your job is to just return the corresponding country from this list:
    {country_list}
    just return the country name, nothing else
    """
    response = model.generate_content(prompt)
    return response.text.strip()



