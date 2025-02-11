from rest_framework import serializers
from .models import Property, LandLocation

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'  # We can include all fields of the Property model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional for updates
        for field in self.fields.values():
            field.required = False


class LandLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLocation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional for updates
        for field in self.fields.values():
            field.required = False