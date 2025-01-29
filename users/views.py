# from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Account, Location
from .serializers import AccountSerializer


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
def protected_view(request):
    return Response({'message': 'You have access to this view!'})


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    Create a new user.
    """
    try:
        # Extract user data from the request
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        date_of_birth = request.data.get('date_of_birth')
        nin = request.data.get('nin')
        password = request.data.get('password')

        # Check if any required fields are missing
        if not all([username, first_name, last_name, email, date_of_birth, nin, password]):
            return Response({'error': 'All required fields must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Account user first
        user = Account.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            nin=nin,
            password=password
        )

        # Extract location data if it exists
        location_data = request.data.get('location')
        if location_data:
            # Ensure all required location fields exist
            required_location_fields = ['village', 'parish', 'subcounty', 'county', 'district']
            if not all(field in location_data for field in required_location_fields):
                return Response({'error': 'All location fields must be provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the location and associate it with the newly created user
            Location.objects.create(account=user, **location_data)

        return Response({
            'message': 'User created successfully',
            'user': AccountSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, username):
    """
    Retrieve user details by username.
    """
    user = get_object_or_404(Account, username=username)
    return Response(AccountSerializer(user).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # This ensures only authenticated users can update
def update_user(request, username):
    """
    Update user information.
    Only the user who is logged in or an admin can update their own data.
    """
    # Ensure the logged-in user is the one being updated
    if request.user.username != username:
        return Response({'error': 'You do not have permission to update this user'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(Account, username=username)
    
    # Update fields from the request
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    user.date_of_birth = request.data.get('date_of_birth', user.date_of_birth)
    user.nin = request.data.get('nin', user.nin)
    
    # If location data is provided, update it
    if 'location' in request.data:
        user.location = request.data['location']
    
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
    update_session_auth_hash(request, user)

    return Response({'message': 'Password updated successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Logout the user by deleting or ignoring the access token.
    """
    return Response({'message': 'You have successfully logged out'})