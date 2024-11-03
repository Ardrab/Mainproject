import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
data = pd.read_csv('models/symptoms_cleaned.csv')

# Split symptoms into a list and clean whitespace
data['symptoms'] = data['symptoms'].apply(lambda x: [symptom.strip() for symptom in x.split(',')])

# Explode the DataFrame to have one symptom per row
data = data.explode('symptoms')

# Create a simple bag-of-words model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['symptoms'])
y = data['disease']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model and vectorizer
joblib.dump(model, 'disease_symptom_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
