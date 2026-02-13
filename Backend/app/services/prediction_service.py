import joblib
import numpy as np
import pandas as pd
from pathlib import Path

class LoanPredictionService:
    """Service for loan prediction using trained ML model"""
    
    def __init__(self):
        """Load trained model and preprocessing objects"""
        model_dir = Path(__file__).parent.parent.parent / 'ml_model'
        
        self.model = joblib.load(model_dir / 'loan_model.pkl')
        self.scaler = joblib.load(model_dir / 'scaler.pkl')
        self.label_encoders = joblib.load(model_dir / 'label_encoders.pkl')
        self.target_encoder = joblib.load(model_dir / 'target_encoder.pkl')
        self.feature_columns = joblib.load(model_dir / 'feature_columns.pkl')
        
        print("✓ ML Model and preprocessors loaded successfully")
    
    def predict(self, profile_data: dict, loan_data: dict) -> dict:
        """
        Make loan approval prediction
        
        Args:
            profile_data: User profile information
            loan_data: Loan details
            
        Returns:
            Dictionary with prediction results and probabilities
        """
        # Map frontend fields to model features
        employment_mapping = {
            'Self-Employed': 'Yes',
            'Employed': 'No',
            'Unemployed': 'No'
        }
        
        # Prepare input data
        input_data = {
            'Gender': profile_data['gender'],
            'Married': loan_data['married'],
            'Dependents': loan_data['dependents'],
            'Education': loan_data['education'],
            'Self_Employed': employment_mapping.get(profile_data['employment_type'], 'No'),
            'ApplicantIncome': int(loan_data['applicant_income']),
            'CoapplicantIncome': int(loan_data['coapplicant_income']),
            'LoanAmount': int(loan_data['loan_amount']),
            'Loan_Amount_Term': loan_data['loan_term'],
            'Credit_History': float(loan_data['credit_history']),
            'Property_Area': loan_data['property_area']
        }
        
        # Create DataFrame
        df = pd.DataFrame([input_data])
        
        # Encode categorical variables
        categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
        for col in categorical_columns:
            if col in self.label_encoders:
                try:
                    df[col] = self.label_encoders[col].transform(df[col])
                except ValueError:
                    # Handle unseen labels
                    df[col] = 0
        
        # Ensure correct column order
        df = df[self.feature_columns]
        
        # Scale features
        X_scaled = self.scaler.transform(df)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)[0]
        prediction_proba = self.model.predict_proba(X_scaled)[0]
        
        # Decode prediction
        prediction_label = self.target_encoder.inverse_transform([prediction])[0]
        
        # Get probabilities
        # Class 0 is 'N' (Rejected), Class 1 is 'Y' (Approved)
        prob_rejected = float(prediction_proba[0])
        prob_approved = float(prediction_proba[1])
        
        # Determine result
        result = {
            'prediction': prediction_label,
            'prediction_label': 'Approved' if prediction_label == 'Y' else 'Rejected',
            'probability_approved': round(prob_approved * 100, 2),
            'probability_rejected': round(prob_rejected * 100, 2),
            'confidence': round(max(prob_approved, prob_rejected) * 100, 2),
            'applicant_name': profile_data['name']
        }
        
        return result

# Singleton instance
prediction_service = None

def get_prediction_service():
    """Get or create prediction service instance"""
    global prediction_service
    if prediction_service is None:
        prediction_service = LoanPredictionService()
    return prediction_service