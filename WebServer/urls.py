from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from WebServer import settings
from scripts import script

urlpatterns = [
                  path('', include('WebSite.urls')),
                  path('api/', include('REST.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

script()