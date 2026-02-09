import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic loan dataset
n_samples = 1000

# Generate features
data = {
    'Gender': np.random.choice(['Male', 'Female'], n_samples, p=[0.65, 0.35]),
    'Married': np.random.choice(['Yes', 'No'], n_samples, p=[0.70, 0.30]),
    'Dependents': np.random.choice(['0', '1', '2', '3+'], n_samples, p=[0.40, 0.30, 0.20, 0.10]),
    'Education': np.random.choice(['Graduate', 'Not Graduate'], n_samples, p=[0.75, 0.25]),
    'Self_Employed': np.random.choice(['Yes', 'No'], n_samples, p=[0.15, 0.85]),
    'ApplicantIncome': np.random.randint(1000, 15000, n_samples),
    'CoapplicantIncome': np.random.randint(0, 8000, n_samples),
    'LoanAmount': np.random.randint(50, 600, n_samples),
    'Loan_Amount_Term': np.random.choice([360, 180, 120, 240, 480], n_samples, p=[0.70, 0.15, 0.05, 0.05, 0.05]),
    'Credit_History': np.random.choice([1.0, 0.0], n_samples, p=[0.85, 0.15]),
    'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n_samples, p=[0.40, 0.35, 0.25])
}

df = pd.DataFrame(data)

# Generate loan status based on logical rules
def generate_loan_status(row):
    score = 0

    # Credit history
    if row['Credit_History'] == 1.0:
        score += 40

    # Income factors
    total_income = row['ApplicantIncome'] + row['CoapplicantIncome']
    if total_income > 10000:
        score += 20
    elif total_income > 5000:
        score += 10

    # Loan to income ratio
    loan_to_income_ratio = row['LoanAmount'] / (total_income / 1000)
    if loan_to_income_ratio < 5:
        score += 15
    elif loan_to_income_ratio < 10:
        score += 5

    # Education
    if row['Education'] == 'Graduate':
        score += 10

    # Employment
    if row['Self_Employed'] == 'No':
        score += 5

    # Property area
    if row['Property_Area'] in ['Urban', 'Semiurban']:
        score += 5

    # Married
    if row['Married'] == 'Yes':
        score += 5

    # Random variation
    score += np.random.randint(-10, 10)

    return 'Y' if score >= 50 else 'N'

df['Loan_Status'] = df.apply(generate_loan_status, axis=1)

# Ensure dataset folder exists
os.makedirs("dataset", exist_ok=True)

# Save dataset (clean relative path)
df.to_csv("dataset/loan_data.csv", index=False)

print("Dataset created successfully!")
print(f"Total samples: {len(df)}")
print(f"Approved loans: {sum(df['Loan_Status'] == 'Y')} ({sum(df['Loan_Status'] == 'Y')/len(df)*100:.1f}%)")
print(f"Rejected loans: {sum(df['Loan_Status'] == 'N')} ({sum(df['Loan_Status'] == 'N')/len(df)*100:.1f}%)")
print("\nDataset preview:")
print(df.head())
