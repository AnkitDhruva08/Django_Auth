from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import json

# Function to register a new user
@api_view(['POST'])
def register_user(request):
    if request.method == "POST":
        print('Data received from frontend for registration:', request.body)
        
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if User.objects.filter(username=username).exists():
            print(f'Username {username} already exists')
            return JsonResponse({"status": "405", "ok": False, "message": "Username already exists"})
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        print(f'User {username} registered successfully')
        
        return JsonResponse({"status": "200", "ok": True, "message": "User registered successfully"})

# Function to login user and generate JWT tokens
@api_view(['POST'])
def login_user(request):
    if request.method == "POST":
        print('Data received from frontend for login:', request.body)
        
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        print('user ===<<<<>>>', user)
        
        if user is not None:
            login(request, user)  # Django session login
            print(f'User {username} authenticated successfully')
            
            refresh = RefreshToken.for_user(user)
            
            # Store refresh token in the database (if required)
            print('Generated Refresh Token:', str(refresh))
            print('Generated Access Token:', str(refresh.access_token))
            
            return Response({
                "status": "200", 
                "ok": True,
                "message": "Login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })
        else:
            print('Invalid credentials for', username)
            return JsonResponse({"status": "401", "ok": False, "message": "Invalid credentials"})

# Function to logout user and remove session
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    print(f'Logging out user: {request.user.username}')
    logout(request)  # Django session logout
    return JsonResponse({"status": "200", "ok": True, "message": "Logout successful"})

# Function to verify if user is authenticated
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_authentication(request):
    print(f'User {request.user.username} is authenticated')
    return JsonResponse({"status": "200", "ok": True, "message": "User is authenticated", "username": request.user.username})


