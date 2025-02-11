from rest_framework import serializers
from .models import Account, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['village', 'parish', 'subcounty', 'county', 'district', 'country']


class AccountSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = Account
        # fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 'date_of_birth', 'nin', 'land_owner', 'surveyor', 'govt_official', 'law_enforcement', 'location']
        fields = '__all__'
