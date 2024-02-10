from django.urls import path

from REST.views import *

urlpatterns = [
    path('vehicles/', VehiclesAPI.as_view(), name='vehicle-api'),
    path('vehicles/<int:vehicle_id>/', VehiclesAPI.as_view(), name='vehicle-api-id'),
    path('alerts/', AlertsAPI.as_view(), name='alert-api'),
    path('contatcs/<int:vehicle_id>', UserAPI.as_view()),
]
