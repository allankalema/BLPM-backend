from rest_framework import serializers
from .models import Account, Location

class BasicAccountSerializer(serializers.ModelSerializer):
    """ Serializer for initial user signup (without roles or location). """
    password = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(required=True)
    nin = serializers.CharField(required=True)

    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'date_of_birth', 'nin']

    def create(self, validated_data):
        """ Create user with hashed password. """
        user = Account.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            date_of_birth=validated_data['date_of_birth'],
            nin=validated_data['nin'],
            password=validated_data['password']
        )
        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['village', 'parish', 'subcounty', 'county', 'district', 'country']


class CompleteAccountSerializer(serializers.ModelSerializer):
    """ Serializer for updating roles and adding location info. """
    location = LocationSerializer(required=False)

    class Meta:
        model = Account
        fields = ['land_owner', 'surveyor', 'govt_official', 'law_enforcement', 'location', 'date_of_birth', 'nin']

    def update(self, instance, validated_data):
        """ Assign user roles and update location. """
        location_data = validated_data.pop('location', None)

        # Update user roles and additional fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create location
        if location_data:
            Location.objects.update_or_create(account=instance, defaults=location_data)

        return instance
