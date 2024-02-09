import geopy.distance
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/')
    vehicles = models.ManyToManyField('Vehicle', related_name='owners')


class Vehicle(models.Model):
    id = models.IntegerField(primary_key=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    smoke = models.FloatField(default=0)
    temperature = models.FloatField(default=0)


class Alert(models.Model):
    sender = models.ForeignKey(Vehicle, related_name='alerts_sent', on_delete=models.CASCADE)
    receivers = models.ManyToManyField(Vehicle, related_name='alerts_received', default=None)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    smoke = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)
    recent = models.BooleanField(default=0)

    def get_alerts_in_range(self, radius):
        """
        Returns all vehicles within a certain radius from this alert.

        :param radius: The radius within which to search for vehicles (in kilometers).
        :return: A queryset containing the vehicles within the specified radius.
        """
        alert_point = (self.latitude, self.longitude)

        vehicles_in_range = []
        for vehicle in Vehicle.objects.exclude(pk=self.sender_id):
            vehicle_point = (vehicle.latitude, vehicle.longitude)
            distance = geopy.distance.geodesic(alert_point, vehicle_point).kilometers
            if distance <= radius:
                vehicles_in_range.append(vehicle)
                print("")

        return vehicles_in_range
