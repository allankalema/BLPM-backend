from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Property, LandLocation
from .serializers import PropertySerializer, LandLocationSerializer

@api_view(['GET'])
def index(request):
    user_id = request.user.get_id()
    properties = Property.objects.filter(owner=user_id, status=1)
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_property(request):
    user_id = request.user.get_id()
    request.data['owner'] = user_id
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        property_instance = serializer.save()
        return Response({"property_id": property_instance.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_land_location(request, property_id):
    """
    Create LandLocation using the property ID.
    """
    try:
        property_instance = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        request.data['property'] = property_instance.id  # Attach the property to the LandLocation
        serializer = LandLocationSerializer(data=request.data)
        if serializer.is_valid():
            land_location_instance = serializer.save()
            return Response({"land_location_id": land_location_instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_property(request):
    """
    Update an existing Property by its ID.
    """
    try:
        property_instance = Property.objects.get(id=request.data['id'])
    except Property.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    
    serializer = PropertySerializer(property_instance, data=request.data, partial=True)  # partial=True allows partial updates
    if serializer.is_valid():
        serializer.save()
        return Response({"property_id": property_instance.id, "message": "Property updated successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_land_location(request, property_id):
    """
    Update the LandLocation for a specific Property using property_id.
    """
    try:
        land_location_instance = LandLocation.objects.get(property__id=property_id)
    except LandLocation.DoesNotExist:
        return Response({"detail": "LandLocation not found for this property."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = LandLocationSerializer(land_location_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"land_location_id": land_location_instance.id, "message": "LandLocation updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])   
def delete_property(request):
    """
    Delete a property by its ID.
    """
    try:
        property_instance = Property.objects.get(id=request.data['id'], status=1)
    except Property.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    property_instance.status = 0
    property_instance.save()
    return Response({"message": "Property deleted successfully."}, status=status.HTTP_200_OK)