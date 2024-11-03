import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from .predict_symptoms import predict_symptoms  # Import your prediction function

# Load symptoms data globally to avoid loading it on each request
symptoms_data = pd.read_csv('healthcare_chatbot/models/symptoms_cleaned.csv')

def chatbot_view(request):
    return render(request, 'healthcare_chatbot/chatbot_interface.html')

def get_symptoms(request):
    if request.method == 'POST':
        disease_name = request.POST.get('disease').strip()  # Strip whitespace
        print("Received disease:", disease_name)  # Debugging line
        
        # Fetch symptoms from the DataFrame
        symptoms = symptoms_data[symptoms_data['disease'].str.strip().str.lower() == disease_name.lower()]['symptoms']
        
        if not symptoms.empty:
            # If symptoms are found in the CSV, return them
            return JsonResponse({'symptoms': symptoms.values[0].split(', ')})
        else:
            # If not found in the CSV, use the prediction model
            predicted_symptoms = predict_symptoms(disease_name)  # Call your prediction function
            
            if len(predicted_symptoms) > 0:
                return JsonResponse({'symptoms': predicted_symptoms})
            else:
                return JsonResponse({'symptoms': 'Disease not found.'})

    return JsonResponse({'symptoms': 'Invalid request method.'})
