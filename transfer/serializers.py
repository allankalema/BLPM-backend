from rest_framework import serializers
from .models import Transfer
from property.models import Property
from django.contrib.auth import get_user_model

User = get_user_model()

class TransferSerializer(serializers.ModelSerializer):
    # Including the username for both users in the response, instead of just the ID
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    land_title = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = Transfer
        fields = ('id', 'from_user', 'to_user', 'land_title', 'status', 'transfer_date')
        read_only_fields = ('transfer_date',)

    def validate(self, data):
        """
        Custom validation if needed, for example, ensuring users are not transferring
        the property to themselves.
        """
        if data['from_user'] == data['to_user']:
            raise serializers.ValidationError("The transfer cannot be made to the same user.")
        return data
