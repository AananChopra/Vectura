from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import json
from .models import ConsultationReport
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import ConsultationReport 
# Add these imports at the top of your file
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors as reportlab_colors


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Request Data:", request.data)  # Debug log

        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name or not email or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data={
            "name": name,
            "email": email,
            "password": password
        })

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)  # 🔍 ADD THIS LINE
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        User = get_user_model()

class LoginView(APIView):
    authentication_classes = []  # No authentication required for login
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=400)

        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "name": user.username,
                "email": user.email
            }
        })
    

def csrf_token_view(request):
    """
    Send a CSRF token to the frontend for session-based authentication.
    Not required for token-based auth, but may be useful in dev/testing.
    """
    token = get_token(request)
    return JsonResponse({"csrfToken": token})

@csrf_exempt  # Only use during development/testing
@require_POST
def logout_view(request):
    """
    Logs out the user by clearing the session.
    Not strictly required for token-based authentication.
    """
    logout(request)
    response = JsonResponse({"message": "Logged out successfully"})
    response.delete_cookie("sessionid")
    return response

# views.py
from .models import ConsultationReport
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt  # CSRF exemption if you're dealing with cross-origin requests
def save_consultation(request):
    if request.method == "POST":
        try:
            # Load the incoming JSON data
            data = json.loads(request.body)

            # Extract necessary data from the request
            responses = data.get("responses", {})
            ml_result = data.get("mlResult", "Not Available")

            # Extract specific fields from the responses
            country = responses.get("3️⃣ Which country do you currently live in?", "")
            monthly_income = responses.get("7️⃣ What is your monthly income? (Exact amount if fixed, or range like ₹50,000–₹90,000)", "")
            
            section3_text = (
                f"{responses.get('8️⃣ What is your average total monthly expense? (Include rent, groceries, utilities, medical bills, etc.)', '')}\n"
                f"{responses.get('9️⃣ Do you own any significant assets or savings? If yes, please estimate their total value.', '')}"
            )

            loan_details = responses.get("🔟 How many loans do you currently have? (Please list each loan in this format: ➤ One loan of ₹X, EMI over Y months at Z% interest per annum.)", "")

            # Create a new consultation report entry in the database
            report = ConsultationReport.objects.create(
                user=request.user if request.user.is_authenticated else None,  # Optionally link to user if authenticated
                responses=responses,
                ml_result=ml_result,
                country=country,
                monthly_income=monthly_income,
                expenses_and_assets=section3_text,
                loan_details=loan_details
            )

            # Return success response with the created report ID
            return JsonResponse({"message": "Consultation report saved successfully", "report_id": report.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in request"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method, expected POST"}, status=400)



def generate_pdf(request, report_id):
    try:
        # Questions array (make sure this matches your React component exactly)
        QUESTIONS = [
            "👋 Welcome Message",  # This won't be displayed in the Q&A table
            "Full Name",
            "Age",
            "Country of Residence",
            "Currency Used (e.g., USD, INR, EUR)",
            "Employment Status",
            "Industry",
            "Monthly Income",
            "Rent/mortagage",
            "Utilities",
            "Food/grocery expenses",
            "Tuition fee",
            "Misclelaneous expenses(e.g., entertainment, shopping, etc.)",
            "Assets/Savings Value",
            "Current Loans",
            "Missed Payment Frequency",
            "Debt Comfort Level (1-5)",
            "Analysis Completion"  # This won't be displayed in the Q&A table
        ]

        # Fetch the financial consultation report
        report = ConsultationReport.objects.get(id=report_id)

        # Create an HTTP response for PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="debt_consultation_report_{report_id}.pdf"'

        # Enhanced color palette
        primary_color = colors.HexColor('#1E88E5')       # Blue
        secondary_color = colors.HexColor('#43A047')     # Green
        text_color = colors.HexColor('#212121')          # Dark grey
        light_bg = colors.HexColor('#F5F5F5')            # Light grey
        accent_color = colors.HexColor('#FF5722')        # Orange accent
        
        # Risk level colors
        very_high_risk_color = colors.HexColor('#FF1744')  # Red
        high_risk_color = colors.HexColor('#FF9100')       # Orange
        moderate_risk_color = colors.HexColor('#FFEB3B')   # Yellow
        low_risk_color = colors.HexColor('#76FF03')        # Light green
        very_low_risk_color = colors.HexColor('#00C853')   # Green

        doc = SimpleDocTemplate(
            response,
            pagesize=letter,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch
        )

        elements = []
        styles = getSampleStyleSheet()

        # Enhanced custom styles
        title_style = ParagraphStyle(
            'TitleStyle', 
            parent=styles['Title'], 
            fontSize=26, 
            textColor=primary_color, 
            alignment=1,  # This centers the text
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'SubtitleStyle', 
            parent=styles['Heading2'], 
            fontSize=18, 
            textColor=secondary_color,
            spaceAfter=10,
            alignment=1  # This centers the text
        )
        
        section_title = ParagraphStyle(
            'SectionTitle', 
            parent=styles['Heading3'], 
            fontSize=15, 
            textColor=text_color, 
            fontName='Helvetica-Bold', 
            spaceBefore=16, 
            spaceAfter=8,
            borderColor=primary_color,
            borderWidth=0,
            borderPadding=5,
            borderRadius=5
        )
        
        body_text = ParagraphStyle(
            'BodyText', 
            parent=styles['Normal'], 
            fontSize=11, 
            textColor=text_color, 
            leading=16
        )
        
        note_style = ParagraphStyle(
            'NoteStyle',
            parent=styles['Italic'],
            fontSize=9,
            textColor=colors.gray,
            alignment=1,
            spaceBefore=6
        )

        # Logo and Header
        logo_text = Paragraph(
            "<font color='#1E88E5' size='28'><b>Ventura</b></font> <font color='#43A047' size='28'>Debt Assistant</font>",
            title_style
        )
        elements.append(logo_text)

        # Centered Subtitle with decorative element
        elements.append(Paragraph(f"Financial Assessment Report #{report.id}", subtitle_style))

        if hasattr(report, 'created_at'):
            date_text = Paragraph(
                f"Generated on: {report.created_at.strftime('%B %d, %Y at %H:%M')}", 
                ParagraphStyle('DateText', parent=body_text, textColor=colors.darkgrey, alignment=1)
            )
            elements.append(date_text)

        elements.append(Spacer(1, 10))

        # Enhanced horizontal separator
        separator = Table([['']], colWidths=[7 * inch])
        separator.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 2, primary_color),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ]))
        elements.append(separator)
        elements.append(Spacer(1, 20))

        # Risk Assessment Section
        elements.append(Paragraph("Risk Assessment", section_title))
        
        # Try to extract risk level from ML model results
        try:
            ml_data = json.loads(report.ml_result)
            risk_level = ml_data.get("risk_level", "N/A")
            risk_percentage = ml_data.get("risk_percentage", "N/A")
        except Exception:
            risk_level = "Moderate Risk"  # Default dummy value
            risk_percentage = "+5.2%"     # Default dummy value
            
        # Risk assessment table
        risk_table_data = [
            [
                Paragraph("<b>Risk Level</b>", body_text), 
                Paragraph("<b>Debt-to-Income Ratio</b>", body_text), 
                Paragraph("<b>Status</b>", body_text)
            ],
            [
                Paragraph("Very High Risk", body_text), 
                Paragraph("+30% or more", body_text), 
                Paragraph("🚨 Critical", body_text)
            ],
            [
                Paragraph("High Risk", body_text), 
                Paragraph("+15% to +29.99%", body_text), 
                Paragraph("⚠ Concerning", body_text)
            ],
            [
                Paragraph("Moderate Risk", body_text), 
                Paragraph("-15% to +14.99%", body_text), 
                Paragraph("⚖ Stable", body_text)
            ],
            [
                Paragraph("Low Risk", body_text), 
                Paragraph("-15.01% to -30%", body_text), 
                Paragraph("✅ Safe", body_text)
            ],
            [
                Paragraph("Very Low Risk", body_text), 
                Paragraph("Lower than -30%", body_text), 
                Paragraph("🟢 Very Stable", body_text)
            ]
        ]
        
        risk_table = Table(risk_table_data, colWidths=[2.33*inch, 2.33*inch, 2.33*inch])
        
        # Color coding for risk levels
        risk_table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            # Risk level colors
            ('BACKGROUND', (0, 1), (0, 1), very_high_risk_color),
            ('BACKGROUND', (0, 2), (0, 2), high_risk_color),
            ('BACKGROUND', (0, 3), (0, 3), moderate_risk_color),
            ('BACKGROUND', (0, 4), (0, 4), low_risk_color),
            ('BACKGROUND', (0, 5), (0, 5), very_low_risk_color),
            # Text colors for colored backgrounds
            ('TEXTCOLOR', (0, 1), (0, 1), colors.white),
            ('TEXTCOLOR', (0, 2), (0, 2), colors.white),
        ]
        
        # Highlight the row corresponding to the user's risk level
        for i in range(1, 6):
            risk_name = risk_table_data[i][0].text.replace("<b>", "").replace("</b>", "")
            if risk_level == risk_name:
                risk_table_style.append(('BACKGROUND', (1, i), (2, i), colors.lightblue))
                risk_table_style.append(('FONTNAME', (1, i), (2, i), 'Helvetica-Bold'))
        
        risk_table.setStyle(TableStyle(risk_table_style))
        elements.append(risk_table)
        
        # Risk level explanation
        risk_explanation = f"Your current risk level: <b>{risk_level}</b> with a debt-to-income ratio of <b>{risk_percentage}</b>"
        elements.append(Paragraph(risk_explanation, 
            ParagraphStyle('RiskExplanation', 
                parent=body_text, 
                fontSize=12, 
                textColor=accent_color, 
                alignment=1,
                spaceBefore=12
            )))
        
        elements.append(Spacer(1, 25))
        
        # Financial Breakdown Pie Chart
        elements.append(Paragraph("Financial Breakdown", section_title))
        elements.append(Spacer(1, 10))

        try:
            # Monthly income
            monthly_income = float(report.responses.get("7", 0))  # Index 7: Monthly Income

            # Individual expenses from responses
            rent = float(report.responses.get("8", 0))
            utilities = float(report.responses.get("9", 0))
            food = float(report.responses.get("10", 0))
            tuition = float(report.responses.get("11", 0))
            misc = float(report.responses.get("12", 0))

            # Total expenses
            monthly_expenses = rent + utilities + food + tuition + misc
            savings = max(0, monthly_income - monthly_expenses)

            # List of all individual expense categories including Savings
            data = [
                ("Rent/Mortgage", rent),
                ("Utilities", utilities),
                ("Food/Groceries", food),
                ("Tuition", tuition),
                ("Miscellaneous", misc),
                ("Savings", savings)
            ]

            # Drawing the pie chart
            drawing = Drawing(width=400, height=200)
            pie = Pie()
            pie.x = 100
            pie.y = 25
            pie.width = 200
            pie.height = 150

            pie.data = [d[1] for d in data]
            pie.labels = [d[0] for d in data]

            pie.slices.strokeWidth = 0.5

            # Assign colors
            slice_colors = [
                accent_color,
                secondary_color,
                high_risk_color,
                very_high_risk_color,
                colors.purple,
                colors.green  # Savings in green
            ]
            for i, color in enumerate(slice_colors):
                if i < len(pie.data):
                    pie.slices[i].fillColor = color

            drawing.add(pie)

            # Add chart title
            elements.append(Paragraph("Monthly Expense Distribution", ParagraphStyle(
                'ChartTitle',
                parent=body_text,
                fontSize=12,
                alignment=1,
                spaceBefore=6,
                spaceAfter=6
            )))

            elements.append(drawing)

            # Summary description below the chart
            if savings > 0:
                chart_desc = f"""
                Monthly Income: ${monthly_income:.2f}<br/>
                Total Monthly Expenses: ${monthly_expenses:.2f}<br/>
                Monthly Savings: ${savings:.2f} ({(savings / monthly_income * 100):.1f}% of income)
                """
            else:
                deficit = abs(monthly_income - monthly_expenses)
                chart_desc = f"""
                Monthly Income: ${monthly_income:.2f}<br/>
                Total Monthly Expenses: ${monthly_expenses:.2f}<br/>
                Monthly Deficit: ${deficit:.2f} ({(deficit / monthly_income * 100):.1f}% over income)
                """

            elements.append(Paragraph(chart_desc, ParagraphStyle(
                'ChartDesc',
                parent=body_text,
                fontSize=10,
                alignment=1,
                spaceBefore=10
            )))

        except Exception as e:
            elements.append(Paragraph("⚠️ Could not generate financial breakdown chart. Error: " + str(e), body_text))
            elements.append(Spacer(1, 25))

        # Summary section with enhanced styling
        elements.append(Paragraph("Financial Summary", section_title))

        try:
            ml_data = json.loads(report.ml_result)
            suggestions = ml_data.get("suggestions", [])
            top_suggestions = ", ".join(s["suggestion"] for s in suggestions)
        except Exception:
            top_suggestions = "Consider establishing an emergency fund, reducing non-essential expenses, and making regular payments on high-interest debt first."

        # Add risk assessment to the summary table
        summary_info = [
            [Paragraph("<b>Report ID:</b>", body_text), Paragraph(str(report.id), body_text)],
            [Paragraph("<b>Risk Assessment:</b>", body_text), Paragraph(f"{risk_level} ({risk_percentage})", body_text)],
            [Paragraph("<b>AI Recommendations:</b>", body_text), Paragraph(top_suggestions, body_text)],
        ]

        summary_table = Table(summary_info, colWidths=[2 * inch, 4.5 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), light_bg),
            ('TEXTCOLOR', (0, 0), (0, -1), text_color),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('ROUNDEDCORNERS', [5]),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 25))

        # Q&A section with improved styling
        if report.responses:
            elements.append(Paragraph("Financial Questionnaire Responses", section_title))
            elements.append(Spacer(1, 8))

            qa_data = [[Paragraph("<b>Question</b>", body_text), Paragraph("<b>Response</b>", body_text)]]

            # Match questions with answers using their indices
            for idx in range(1, len(QUESTIONS) - 1):  # Skip welcome message and completion
                question = QUESTIONS[idx]
                answer = report.responses.get(str(idx), "No answer provided")
                qa_data.append([
                    Paragraph(question, body_text),
                    Paragraph(str(answer), body_text)
                ])

            qa_table = Table(qa_data, colWidths=[3.25 * inch, 3.25 * inch])

            # Table style with enhanced alternating colors
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ]
            for i in range(1, len(qa_data)):
                bg = light_bg if i % 2 == 0 else colors.white
                table_style.append(('BACKGROUND', (0, i), (-1, i), bg))

            qa_table.setStyle(TableStyle(table_style))
            elements.append(qa_table)
            elements.append(Spacer(1, 25))

        # Additional notes section
        elements.append(Paragraph("Additional Notes", section_title))
        
        notes_text = """
        The risk assessment is based on your debt-to-income ratio and other financial factors. 
        This report provides a snapshot of your current financial situation and offers personalized 
        recommendations to improve your financial health.
        """
        elements.append(Paragraph(notes_text, body_text))
        elements.append(Spacer(1, 20))

        # Enhanced disclaimer with box styling
        disclaimer_style = ParagraphStyle(
            'Disclaimer', 
            parent=styles['Italic'], 
            fontSize=9, 
            textColor=text_color, 
            alignment=1,
            borderColor=colors.lightgrey,
            borderWidth=1,
            borderPadding=10,
            backColor=colors.whitesmoke
        )
        
        disclaimer = Paragraph(
            "DISCLAIMER: This financial report is AI-generated for assessment purposes only and does not constitute professional "
            "financial advice. Please consult with a qualified financial advisor before making any financial decisions.",
            disclaimer_style
        )
        elements.append(disclaimer)
        elements.append(Spacer(1, 20))

        # Enhanced footer
        footer_separator = Table([['']], colWidths=[7 * inch])
        footer_separator.setStyle(TableStyle([('LINEABOVE', (0, 0), (-1, 0), 1, colors.lightgrey)]))
        elements.append(footer_separator)

        footer = Paragraph(
            "Thank you for using <font color='#1E88E5'><b>Ventura</b></font> | Your AI Financial Assistant",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10, textColor=secondary_color, alignment=1)
        )
        elements.append(Spacer(1, 10))
        elements.append(footer)

        # Build the PDF
        doc.build(elements)
        return response

    except ConsultationReport.DoesNotExist:
        return HttpResponse("Report not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)