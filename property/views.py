from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Property, LandLocation
from .serializers import PropertySerializer, LandLocationSerializer

@api_view(['POST'])
def create_property(request):
    """
    Create Property and return the created property ID.
    """
    if request.method == 'POST':
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            property_instance = serializer.save()
            return Response({"property_id": property_instance.id}, status=status.HTTP_201_CREATED)
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


@api_view(['PUT'])
def update_property(request, property_id):
    """
    Update an existing Property by its ID.
    """
    try:
        property_instance = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
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