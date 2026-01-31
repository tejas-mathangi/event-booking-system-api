from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
def register(request):
    """
    Creates a user and returns JWT tokens (access + refresh)
    """
    username = request.data.get("username")
    email = request.data.get("email", "")
    password = request.data.get("password")

    # basic validations
    if not username or not password:
        return Response(
            {"error": "username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # create user
    user = User.objects.create_user(username=username, email=email, password=password)

    # create JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "message": "user registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_201_CREATED
    )
