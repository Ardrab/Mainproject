from django.shortcuts import render
from django.http import JsonResponse

# Dummy function to simulate disease prediction
def predict_disease(result_values):
    if result_values['sugar'] > 200:
        return "Diabetes"
    elif result_values['blood_pressure'] > 140:
        return "Hypertension"
    elif result_values['cholesterol'] > 240:
        return "High Cholesterol"
    else:
        return "Healthy"

# Dictionary to hold diseases and their symptoms
disease_symptoms = {
    "hypertension": "Common symptoms include headaches, shortness of breath, and nosebleeds.",
    "diabetes": "Common symptoms include increased thirst, frequent urination, and fatigue.",
    "cholesterol": "High cholesterol usually has no symptoms, but it can lead to heart disease.",
    "asthma": "Symptoms include wheezing, coughing, chest tightness, and shortness of breath.",
    "allergy": "Common symptoms include sneezing, itching, runny nose, and hives.",
    "arthritis": "Symptoms include joint pain, stiffness, swelling, and decreased range of motion.",
    "heart disease": "Symptoms can include chest pain, shortness of breath, and fatigue.",
    "stroke": "Symptoms include sudden numbness, confusion, trouble speaking, and severe headache.",
    "cancer": "Symptoms vary by type but can include unexplained weight loss, fatigue, and pain.",
    "anemia": "Common symptoms include fatigue, weakness, and pale skin.",
    "depression": "Symptoms include persistent sadness, loss of interest, and fatigue.",
    "anxiety": "Symptoms can include excessive worry, restlessness, and difficulty concentrating.",
    "gout": "Symptoms include sudden, severe pain in a joint, often the big toe.",
    "pneumonia": "Symptoms include cough, fever, chills, and difficulty breathing.",
    "tuberculosis": "Symptoms include a persistent cough, weight loss, and night sweats.",
    "hepatitis": "Symptoms can include fatigue, jaundice, and abdominal pain.",
    "kidney disease": "Symptoms include fatigue, swelling, and changes in urination.",
    "thyroid disease": "Symptoms can include weight changes, fatigue, and mood swings.",
    "multiple sclerosis": "Symptoms can include fatigue, difficulty walking, and numbness.",
    "Parkinson's disease": "Symptoms include tremors, stiffness, and difficulty with balance.",
    "Alzheimer's disease": "Symptoms include memory loss, confusion, and difficulty with language."
}

def chatbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        
        # Check if the input is a query or result values
        if user_input.lower().startswith("blood pressure") or user_input.lower().startswith("cholesterol") or user_input.lower().startswith("sugar"):
            # Extract result values from the input
            try:
                # Split the input by commas and strip whitespace
                parts = [part.strip() for part in user_input.split(',')]
                result_values = {}
                
                for part in parts:
                    key_value = part.split(':')
                    if len(key_value) == 2:
                        key = key_value[0].strip().lower()  # Get the key and convert to lowercase
                        value = float(key_value[1].strip())  # Convert the value to float
                        result_values[key] = value
                
                # Check if all required keys are present
                if 'blood pressure' in result_values and 'cholesterol' in result_values and 'sugar' in result_values:
                    prediction = predict_disease(result_values)
                    return JsonResponse({'response': f'Prediction: {prediction}'})
                else:
                    return JsonResponse({'response': 'Invalid result format. Use "blood pressure: value, cholesterol: value, sugar: value"'})
            except (IndexError, ValueError) as e:
                # Log the error for debugging
                print(f"Error processing input: {e}")
                return JsonResponse({'response': 'Invalid result format. Use "blood pressure: value, cholesterol: value, sugar: value"'})
        
        # Handle general queries for symptoms
        if "symptoms" in user_input.lower() or "what is" in user_input.lower():
            disease_name = user_input.lower().replace("what are the symptoms of ", "").strip()
            if disease_name in disease_symptoms:
                return JsonResponse({'response': disease_symptoms[disease_name]})
            else:
                return JsonResponse({'response': 'I can provide information on hypertension, diabetes, cholesterol, and more. Please specify.'})
        
        return JsonResponse({'response': 'I am here to help! Please enter your test results or ask a question.'})

    return render(request, 'chatbot/chatbot.html')