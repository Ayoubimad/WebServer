from django.urls import path

from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Alternate URL for home page
    path('home/', views.home, name='home'),
    # Login page
    path('login/', views.login_view, name='login'),
    # Registration page
    path('register/', views.register_view, name='register'),
    # Logout page
    path('logout/', views.logout_view, name='logout'),
    # Notifications page
    path('notifications/', views.notifications, name='notifications'),
    # Delete alert endpoint
    path('delete_alert/', views.delete_alert, name='delete_alert'),
    # Contacts page
    path('contacts/', views.contacts, name='contacts')
]
