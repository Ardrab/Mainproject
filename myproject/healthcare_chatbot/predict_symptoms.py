import joblib
import pandas as pd

# Load the model and vectorizer
model = joblib.load('healthcare_chatbot/disease_symptom_model.pkl')
vectorizer = joblib.load('healthcare_chatbot/vectorizer.pkl')

def predict_symptoms(disease_name):
    # Prepare the input for prediction
    input_data = [disease_name]
    input_vector = vectorizer.transform(input_data)
    
    # Make predictions
    predicted = model.predict(input_vector)

    if len(predicted) > 0:
        # Ensure predicted output is handled correctly
        predicted_symptoms = []
        
        # Extract the predicted disease from the model
        predicted_disease = predicted[0]  # Get the first (and likely only) prediction
        
        # Load the symptoms data
        symptoms_data = pd.read_csv('healthcare_chatbot/models/symptoms_cleaned.csv')
        
        # Find symptoms associated with the predicted disease
        symptoms_row = symptoms_data[symptoms_data['disease'].str.strip().str.lower() == predicted_disease.lower()]
        
        if not symptoms_row.empty:
            # Return symptoms as a list
            predicted_symptoms = symptoms_row['symptoms'].values[0].split(', ')
        
        return predicted_symptoms

    return []

# Test the function
if __name__ == "__main__":
    test_disease = "Heart Attack"  # Replace with a disease you want to test
    symptoms = predict_symptoms(test_disease)
    print(f"Predicted symptoms for {test_disease}: {symptoms}")
