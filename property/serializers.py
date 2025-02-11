from rest_framework import serializers
from .models import Property, LandLocation

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'land_title', 'title_number', 'title_document', 'owner', 'total_area', 'reference_point', 'date_surveyed')

class LandLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLocation
        fields = ('id', 'property', 'latitude', 'longitude', 'altitude', 'village', 'parish', 'subcounty', 'county', 'district', 'country')
