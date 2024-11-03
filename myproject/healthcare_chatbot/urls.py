from django.urls import path
from .views import chatbot_view, get_symptoms

urlpatterns = [
    path('', chatbot_view, name='chatbot_view'),  # This is the chatbot view
    path('get_symptoms/', get_symptoms, name='get_symptoms'),
]