from pydantic import BaseModel, Field, validator
from typing import Literal

class UserProfile(BaseModel):
    """User profile data schema"""
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=100)
    gender: Literal['Male', 'Female']
    employment_type: Literal['Employed', 'Self-Employed', 'Unemployed']
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class LoanDetails(BaseModel):
    """Loan application details schema"""
    applicant_income: float = Field(..., gt=0, le=100000)
    coapplicant_income: float = Field(..., ge=0, le=100000)
    loan_amount: float = Field(..., gt=0, le=10000)
    loan_term: Literal[120, 180, 240, 360, 480]
    credit_history: Literal[0, 1]
    dependents: Literal['0', '1', '2', '3+']
    property_area: Literal['Urban', 'Semiurban', 'Rural']
    married: Literal['Yes', 'No']
    education: Literal['Graduate', 'Not Graduate']

class LoanPredictionRequest(BaseModel):
    """Complete loan prediction request schema"""
    profile: UserProfile
    loan_details: LoanDetails

class PredictionResult(BaseModel):
    """Prediction result schema"""
    prediction: str
    prediction_label: str
    probability_approved: float
    probability_rejected: float
    confidence: float
    applicant_name: str

class ContactMessage(BaseModel):
    """Contact form schema"""
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    subject: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=10, max_length=1000)
    
    @validator('name', 'subject', 'message')
    def validate_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()