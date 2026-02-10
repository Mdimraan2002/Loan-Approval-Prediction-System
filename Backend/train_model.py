import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# ==============================
# Load Dataset (Relative Path)
# ==============================
df = pd.read_csv('dataset/loan_data.csv')

print("Dataset loaded successfully!")
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")

# Handle missing values (in case any exist)
df = df.dropna()

# Separate features and target
X = df.drop('Loan_Status', axis=1)
y = df['Loan_Status']

# Store original columns for later use
feature_columns = X.columns.tolist()

# Encode categorical variables
label_encoders = {}
categorical_columns = [
    'Gender', 
    'Married', 
    'Dependents', 
    'Education', 
    'Self_Employed', 
    'Property_Area'
]

for col in categorical_columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Encode target variable
le_target = LabelEncoder()
y = le_target.fit_transform(y)

print(f"\nTarget classes: {le_target.classes_}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==============================
# Train Logistic Regression Model
# ==============================
print("\n" + "="*50)
print("Training Logistic Regression Model...")
print("="*50)

model = LogisticRegression(random_state=42, max_iter=1000, solver='lbfgs')
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le_target.classes_))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature importance (coefficients)
print("\nFeature Importance (Coefficients):")
coefficients = pd.DataFrame({
    'Feature': feature_columns,
    'Coefficient': model.coef_[0]
}).sort_values('Coefficient', ascending=False)
print(coefficients)

# ==============================
# Save Model and Preprocessing Objects
# ==============================
model_dir = 'backend/ml_model'

# Create directory if it doesn't exist
os.makedirs(model_dir, exist_ok=True)

print("\n" + "="*50)
print("Saving model and preprocessing objects...")
print("="*50)

joblib.dump(model, os.path.join(model_dir, 'loan_model.pkl'))
joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
joblib.dump(label_encoders, os.path.join(model_dir, 'label_encoders.pkl'))
joblib.dump(le_target, os.path.join(model_dir, 'target_encoder.pkl'))
joblib.dump(feature_columns, os.path.join(model_dir, 'feature_columns.pkl'))

print("\nModel saved successfully!")
print(f"Location: {model_dir}")
print("\nFiles saved:")
print("  - loan_model.pkl (Logistic Regression model)")
print("  - scaler.pkl (StandardScaler)")
print("  - label_encoders.pkl (LabelEncoders for categorical features)")
print("  - target_encoder.pkl (LabelEncoder for target)")
print("  - feature_columns.pkl (Feature column names)")

print("\n" + "="*50)
print("Training Complete!")
print("="*50)
