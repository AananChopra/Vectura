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