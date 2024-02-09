from django.urls import path

from REST.views import *

urlpatterns = [
    path('vehicles/', VehiclesAPI.as_view(), name='vehicle-api'),
    path('vehicles/<int:vehicle_id>/', VehiclesAPI.as_view(), name='vehicle-api-id'),
]
