# from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Account, Location
from .serializers import *


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def checkUserName(request, username):
    if not username:
        return Response({"error": "Username is required"}, status=400)

    is_available = not Account.objects.filter(username=username).exists()
    return Response({"available": is_available}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Phase 1: User signup - Creates an account with basic details.
    """
    serializer = BasicAccountSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Account created successfully. Proceed to complete profile.',
            'user_id': user.id  # Send user_id for phase 2
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_profile(request):
    """
    Phase 2: Assigns roles (surveyor, land owner, etc.) and updates location.
    """
    user = request.user  # The logged-in user
    serializer = CompleteAccountSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated successfully!'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user(request, username):
    """
    Retrieve user details by username.
    """
    user = get_object_or_404(Account, username=username)
    return Response(AccountSerializer(user).data)


@api_view(['POST'])
def update_user(request):
    """
    Update user information.
    Only the user who is logged in or an admin can update their own data.
    """

    username = request.data.get('username')
    if request.user.username != username:
        return Response({'error': 'You do not have permission to update this user'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(Account, username=username)
    
    # Update fields from the request
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    # user.date_of_birth = request.data.get('date_of_birth', user.date_of_birth)
    # user.nin = request.data.get('nin', user.nin)
    
    # # If location data is provided, update it
    # if 'location' in request.data:
    #     user.location = request.data['location']
    
    # Save the changes
    user.save()

    return Response({
        'message': 'User updated successfully',
        'user': AccountSerializer(user).data
    })


    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    """
    Update the user's password.
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    if old_password == new_password:
        return Response({'error': 'New password must be different from the old password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    # Ensure the user session is updated with the new password
    # update_session_auth_hash(request, user)

    return Response({'message': 'Password updated successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Logout the user by deleting or ignoring the access token.
    """
    return Response({'message': 'You have successfully logged out'})