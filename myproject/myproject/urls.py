# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('', include('myapp.urls')),  # Include your app's URLs
    # Add more URL patterns for other apps or views in your project
     path('chatbot/', include('chatbot.urls')),  # Ensure this line is present# Include chatbot URLs
     path('accounts/', include('allauth.urls')),
   
    path('healthchatbot/', include('healthcare_chatbot.urls')),  # Include healthcare_chatbot URLs
    # Other paths...
]
# Include chatbot URLs# Include the healthcare chatbot app URLs