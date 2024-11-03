import pandas as pd
import os

def clean_csv(input_file, output_file):
    # Load the dataset
    data = pd.read_csv(input_file)

    # Strip whitespace from the 'disease' column
    data['disease'] = data['disease'].str.strip()

    # Save the cleaned dataset back to CSV
    data.to_csv(output_file, index=False)

    print(f"Unwanted spaces removed and data saved to {output_file}")

if __name__ == "__main__":
    # Use the absolute path to avoid confusion
    input_file = os.path.join(os.path.dirname(__file__), 'models', 'symptoms.csv')
    output_file = os.path.join(os.path.dirname(__file__), 'models', 'symptoms_cleaned.csv')

    clean_csv(input_file, output_file)
