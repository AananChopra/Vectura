💸 Ventura - AI-Powered Debt Assistant
Ventura is an intelligent debt consultation assistant that guides users through a personalized financial questionnaire, analyzes their responses, and generates a detailed consultation report in PDF format. Designed for individuals seeking to understand and manage their debt more effectively, Ventura offers insights through a conversational interface powered by AI.

🧠 Features:

🤖 Conversational Chatbot – Friendly chatbot (Ventura) guides users through structured financial questions.
📊 Smart Financial Analysis – Automatically parses responses to calculate income vs. expenses.
📄 PDF Report Generation – Generates a downloadable PDF report summarizing:
      >User profile (name, age, income, etc.)
      >Financial breakdown (monthly income vs. expenses)
      >Diagnosis (e.g. financial strain, budgeting advice)
📉 Visual Breakdown – Includes pie chart of income distribution for better clarity.
🔐 Secure Backend – Django-powered API stores and processes consultation data.

🛠️ Tech Stack
Frontend: React + Tailwind CSS
Backend: Django + Django REST Framework
PDF Generation: ReportLab
AI Integration: Conversational logic simulating a financial advisor
Visualization: Matplotlib for pie chart generation

🚀 How It Works
User opens the chatbot interface.
Ventura asks a series of financial questions in a friendly, human-like tone.
User's responses are sent to the Django backend.
Backend analyzes the data and generates a downloadable PDF report.
User receives insights and recommendations based on their input.


📸 Screenshots


🧪 Setup Instructions

1. Clone the Repo
    git clone https://github.com/your-username/vectura.git
    cd vectura

2. Backend Setup
    cd backend
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

3. Frontend Setup
    cd frontend
    npm install
    npm run dev    
    

🧑‍💻 Author
Manasveer Singh Basra
B.Tech CSE @ Manipal University Jaipur
github @Ambarsariya07

