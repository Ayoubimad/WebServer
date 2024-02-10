import json
import os
from datetime import timedelta
from sqlite3 import IntegrityError

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from REST.models import User, Alert, Contact


@login_required(login_url='login/')
def home(request):
    """
    View function for the home page.

    Displays the user's home page after login.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object.
    """
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, "home.html", context)


@login_required(login_url='login/')
def notifications(request):
    """
    View function for the notifications page.

    Displays the notifications for the logged-in user.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object.
    """
    user = User.objects.get(id=request.user.id)
    user_vehicle = user.vehicles.first()  # Get user's first vehicle (simulated, will be retrieved from the user's vehicles)
    if user_vehicle is not None:
        user_alerts = user_vehicle.alerts_received.all()

        # Calculate timestamp for half an hour ago
        half_hour_ago = timezone.now() - timedelta(minutes=30)

        # Iterate through alerts to mark recent ones
        for alert in user_alerts:
            alert.recent = alert.date > half_hour_ago  # Set True if alert's date is recent
    else:
        user_alerts = None

    context = {
        'user': user,
        'user_alerts': user_alerts,
    }
    return render(request, "notifications.html", context)


@csrf_exempt
def delete_alert(request):
    """
    View function to delete an alert.

    Deletes an alert with the specified ID.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object.
    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            alert_id = int(data["alert_id"])
            alert = get_object_or_404(Alert, id=alert_id)
            alert.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)


def login_view(request):
    """
    View function for the login page.

    Handles user authentication and login.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


@login_required(login_url='login/')
def logout_view(request):
    """
    View function for user logout.

    Logs out the user.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponseRedirect object.
    """
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register_view(request):
    """
    View function for the registration page.

    Handles user registration.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object.
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        profile = request.FILES.get("profile")
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.profile_pic = profile or os.path.join("..", "static", "images", "no_pic.png")
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return redirect('home')
    else:
        return render(request, "register.html")


@login_required(login_url='login/')
def contacts(request):
    """
    View function for the contacts page.

    Displays and handles user contacts.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object.
    """
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        prefix = request.POST.get("prefix")
        phone_number = prefix + phone_number
        if phone_number:
            contact, created = Contact.objects.get_or_create(phoneNumber=phone_number)
            user.contacts.add(contact)
            user.save()
            contacts = user.contacts.all()
            return render(request, "contacts.html", {"contacts": contacts})
    contacts = user.contacts.all()
    return render(request, "contacts.html", {"contacts": contacts})


def custom_404(request, exception):
    return render(request, '404.html', status=404)
