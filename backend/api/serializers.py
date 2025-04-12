from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

User = get_user_model()

# 1. User Serializer (for fetching logged-in user details)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

# 2. Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)  # Accept 'name' field to map to username internally

    class Meta:
        model = User
        fields = ["email", "password", "name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        validated_data["username"] = validated_data.pop("name")  # Assign username from 'name'
        user = User.objects.create_user(**validated_data)
        return user

# 3. Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Optional: generate JWT token
        refresh = RefreshToken.for_user(user)
        return {
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
