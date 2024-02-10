from rest_framework import serializers

from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vehicle model.
    """

    class Meta:
        model = Vehicle
        fields = '__all__'  # Include all fields of the Vehicle model


class AlertSerializer(serializers.ModelSerializer):
    """
    Serializer for the Alert model.
    """

    class Meta:
        model = Alert
        fields = ['sender', 'latitude', 'longitude', 'smoke', 'temperature']
        # Include only the specified fields of the Alert model
