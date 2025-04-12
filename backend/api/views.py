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

@csrf_exempt
def save_consultation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        responses = data.get("responses", {})
        ml_result = data.get("mlResult", "Not Available")

        # Extract fields based on updated selection
        country = responses.get("3️⃣ Which country do you currently live in?", "")
        monthly_income = responses.get("7️⃣ What is your monthly income? (Exact amount if fixed, or range like ₹50,000–₹90,000)", "")
        
        section3_text = (
            f"{responses.get('8️⃣ What is your average total monthly expense? (Include rent, groceries, utilities, medical bills, etc.)', '')}\n"
            f"{responses.get('9️⃣ Do you own any significant assets or savings? If yes, please estimate their total value.', '')}"
        )

        loan_details = responses.get("🔟 How many loans do you currently have? (Please list each loan in this format: ➤ One loan of ₹X, EMI over Y months at Z% interest per annum.)", "")

        report = ConsultationReport.objects.create(
            user=request.user if request.user.is_authenticated else None,
            responses=responses,
            ml_result=ml_result,
            country=country,
            monthly_income=monthly_income,
            expenses_and_assets=section3_text,
            loan_details=loan_details
        )

        return JsonResponse({"message": "Consultation report saved successfully", "report_id": report.id})


def generate_pdf(request, report_id):
    try:
        # Fetch the financial consultation report
        report = ConsultationReport.objects.get(id=report_id)

        # Create an HTTP response for PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="debt_consultation_report_{report_id}.pdf"'

        # Color palette
        primary_color = colors.HexColor('#1E88E5')  # Blue
        secondary_color = colors.HexColor('#43A047')  # Green
        text_color = colors.HexColor('#212121')
        light_bg = colors.HexColor('#F5F5F5')

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

        # Custom styles
        title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=24, textColor=primary_color, alignment=1)
        subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Heading2'], fontSize=18, textColor=secondary_color)
        section_title = ParagraphStyle('SectionTitle', parent=styles['Heading3'], fontSize=14, textColor=text_color, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
        body_text = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10, textColor=text_color, leading=14)

        # Header
        header = Paragraph(
            "<font color='#1E88E5'><b>Ventura</b></font> <font color='#43A047'>Debt Assistant</font>",
            title_style
        )
        elements.append(header)

        # Subtitle
        elements.append(Paragraph(f"Financial Assessment Report #{report.id}", subtitle_style))

        if hasattr(report, 'created_at'):
            elements.append(Paragraph(f"Generated on: {report.created_at.strftime('%B %d, %Y at %H:%M')}", body_text))

        elements.append(Spacer(1, 20))

        # Horizontal separator
        separator = Table([['']], colWidths=[7 * inch])
        separator.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, 0), 1, primary_color)]))
        elements.append(separator)
        elements.append(Spacer(1, 20))

        # Summary section
        elements.append(Paragraph("Summary of Results", section_title))

        try:
            ml_data = json.loads(report.ml_result)
            suggestions = ml_data.get("suggestions", [])
            top_suggestions = ", ".join(s["suggestion"] for s in suggestions)
        except Exception:
            top_suggestions = "N/A"

        summary_info = [
            [Paragraph("<b>Report ID:</b>", body_text), Paragraph(str(report.id), body_text)],
            [Paragraph("<b>AI Suggestions:</b>", body_text), Paragraph(top_suggestions, body_text)],
        ]

        summary_table = Table(summary_info, colWidths=[2 * inch, 4.5 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), light_bg),
            ('TEXTCOLOR', (0, 0), (0, -1), text_color),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 30))

        # Q&A section
        if report.responses:
            elements.append(Paragraph("Financial Questionnaire", section_title))
            elements.append(Spacer(1, 6))

            qa_data = [[Paragraph("<b>Question</b>", body_text), Paragraph("<b>Answer</b>", body_text)]]

            for question, answer in report.responses.items():
                qa_data.append([Paragraph(question, body_text), Paragraph(answer, body_text)])

            qa_table = Table(qa_data, colWidths=[3.25 * inch, 3.25 * inch])

            # Table style with alternating colors
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ]
            for i in range(1, len(qa_data)):
                bg = light_bg if i % 2 == 0 else colors.white
                table_style.append(('BACKGROUND', (0, i), (-1, i), bg))

            qa_table.setStyle(TableStyle(table_style))
            elements.append(qa_table)
            elements.append(Spacer(1, 30))

        # Disclaimer
        disclaimer = Paragraph(
            "This financial report is AI-generated for assessment purposes only and does not constitute professional financial advice.",
            ParagraphStyle('Disclaimer', parent=styles['Italic'], fontSize=8, textColor=colors.grey, alignment=1)
        )
        elements.append(disclaimer)
        elements.append(Spacer(1, 12))

        # Footer
        footer_separator = Table([['']], colWidths=[7 * inch])
        footer_separator.setStyle(TableStyle([('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.lightgrey)]))
        elements.append(footer_separator)

        footer = Paragraph(
            "Thank you for using <b>Ventura</b> | Your AI Financial Assistant",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=secondary_color, alignment=1)
        )
        elements.append(Spacer(1, 8))
        elements.append(footer)

        # Build the PDF
        doc.build(elements)
        return response

    except ConsultationReport.DoesNotExist:
        return HttpResponse("Report not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
