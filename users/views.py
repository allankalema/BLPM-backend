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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_location(request):
    """
    Create location for a specific user.
    The user ID is included in the request JSON.
    """
    user = request.user  # The logged-in user
    
    # Ensure that the user ID in the request matches the logged-in user's ID
    user_id = request.data.get('user_id')
    if user_id != user.id:
        return Response({'error': 'User ID mismatch'}, status=status.HTTP_400_BAD_REQUEST)

    # Extract location data from the request
    location_data = {
        'village': request.data.get('village'),
        'parish': request.data.get('parish'),
        'subcounty': request.data.get('subcounty'),
        'county': request.data.get('county'),
        'district': request.data.get('district'),
        'country': request.data.get('country', 'Uganda'),  # Default to Uganda if no country is provided
    }

    # Create the location and associate it with the user
    location = Location.objects.create(account=user, **location_data)
    
    return Response({'message': 'Location created successfully!', 'location': LocationSerializer(location).data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_user(request, username):
    """
    Retrieve user details by username.
    """
    user = get_object_or_404(Account, username=username)
    return Response(AccountSerializer(user).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    Update user information based on user ID.
    """
    user_id = request.data.get('id')  # Retrieve the user ID
    user = get_object_or_404(Account, id=user_id)

    # Serialize and update the user's details
    serializer = AccountUpdateSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'User updated successfully',
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_location(request):
    """
    Update location information based on user ID.
    """
    user_id = request.data.get('id')  # Retrieve the user ID
    location = get_object_or_404(Location, account__id=user_id)  # Get location related to the user ID

    # Serialize and update the location details
    serializer = LocationUpdateSerializer(location, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Location updated successfully',
            'location': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    """
    Update the password of a user.
    """
    user = request.user  # Get the currently logged-in user

    # Validate the serializer with the old password and new password
    serializer = PasswordUpdateSerializer(data=request.data)

    if serializer.is_valid():
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Check if the old password matches
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the password
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Logout the user by deleting or ignoring the access token.
    """
    return Response({'message': 'You have successfully logged out'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Logout the user by simply disregarding the access token.
    This means the token will no longer be valid as the user must log in again.
    """
    # Here we could also add the logic for blacklisting the token if using a blacklist.
    # In the case of JWT, we generally don't store anything server-side, so no action is needed.
    
    return Response({'message': 'You have successfully logged out'}, status=status.HTTP_200_OK)