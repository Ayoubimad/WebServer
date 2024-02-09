from rest_framework import serializers

from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['sender', 'latitude', 'longitude', 'smoke', 'temperature']


"""
    sender = models.ForeignKey(Vehicle, related_name='alerts_sent', on_delete=models.CASCADE)
    receivers = models.ManyToManyField(Vehicle, related_name='alerts_received')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    smoke = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)
    recent = models.BooleanField(default=0)
"""
