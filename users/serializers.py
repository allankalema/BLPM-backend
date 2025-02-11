from rest_framework import serializers
from .models import Account, Location
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

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


class AccountUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for updating user details. """
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'nin', 'land_owner', 'surveyor', 'govt_official', 'law_enforcement']
        
    def update(self, instance, validated_data):
        """ Update the user fields based on the provided data. """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LocationUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for updating location details. """
    class Meta:
        model = Location
        fields = ['village', 'parish', 'subcounty', 'county', 'district', 'country']
        
    def update(self, instance, validated_data):
        """ Update the location fields. """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        """ Validate the new password strength. """
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value