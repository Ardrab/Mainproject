# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('', include('myapp.urls')),  # Include your app's URLs
    # Add more URL patterns for other apps or views in your project
  
     path('accounts/', include('allauth.urls')),
]
