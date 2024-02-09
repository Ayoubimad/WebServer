from django.http import Http404, HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from REST.models import Vehicle, Alert
from REST.serializers import VehicleSerializer, AlertSerializer


def get_vehicle_object(vehicle_id):
    """Get a vehicle object by its ID.

    Args:
        vehicle_id (int): The ID of the vehicle to retrieve.

    Raises:
        Http404: If the vehicle with the specified ID does not exist.

    Returns:
        Vehicle: The vehicle object.
    """
    try:
        return Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        raise Http404


class VehiclesAPI(APIView):
    """API endpoint for handling vehicle instances."""

    def get(self, request, vehicle_id=None):
        """Handle GET requests.

        Args:
            request: The request object.
            vehicle_id (int, optional): The ID of the vehicle to retrieve.

        Returns:
            JsonResponse: JSON response containing vehicle data.
        """
        if vehicle_id is not None:
            vehicle = get_vehicle_object(vehicle_id)
            serializer = VehicleSerializer(vehicle)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            vehicles = Vehicle.objects.all()
            serializer = VehicleSerializer(vehicles, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def put(self, request, vehicle_id):
        """Handle PUT requests.

        Args:
            request: The request object.
            vehicle_id (int): The ID of the vehicle to update.

        Returns:
            HttpResponse: HTTP response indicating success or failure.
        """
        vehicle = get_vehicle_object(vehicle_id)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vehicle_id):
        """Handle DELETE requests.

        Args:
            request: The request object.
            vehicle_id (int): The ID of the vehicle to delete.

        Returns:
            HttpResponse: HTTP response indicating success or failure.
        """
        try:
            vehicle = get_vehicle_object(vehicle_id)
            vehicle.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Handle POST requests.

        Args:
            request: The request object.

        Returns:
            HttpResponse: HTTP response indicating success or failure.
        """
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class AlertsAPI(APIView):

    def get(self, request):
        """Handle GET requests.

        Args:
            request: The request object.

        Returns:
            JsonResponse: JSON response containing alerts data.
        """

        vehicles = Alert.objects.all()
        serializer = AlertSerializer(vehicles, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        """Handle POST requests.

        Args:
            request: The request object.

        Returns:
            HttpResponse: HTTP response indicating success or failure.
        """
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            # Otteniamo i veicoli nel raggio di 5 km dall'alert
            alert = serializer.save()
            vehicles_in_range = alert.get_alerts_in_range(radius=5)
            # Associazione degli alert solo con i veicoli nel raggio
            alert.receivers.set(vehicles_in_range)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
