from fastapi import APIRouter, HTTPException
from app.schemas.schemas import LoanPredictionRequest, PredictionResult, ContactMessage
from app.services.prediction_service import get_prediction_service

router = APIRouter(prefix="/api", tags=["predictions"])

@router.post("/predict", response_model=PredictionResult)
async def predict_loan(request: LoanPredictionRequest):
    """
    Predict loan approval status based on user profile and loan details
    """
    try:
        # Get prediction service
        service = get_prediction_service()
        
        # Convert Pydantic models to dictionaries
        profile_data = request.profile.dict()
        loan_data = request.loan_details.dict()
        
        # Make prediction
        result = service.predict(profile_data, loan_data)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/contact")
async def submit_contact(contact: ContactMessage):
    """
    Handle contact form submission
    """
    try:
        # In a real application, you would:
        # - Save to database
        # - Send email notification
        # - Log the inquiry
        
        return {
            "success": True,
            "message": f"Thank you {contact.name}! We have received your message and will get back to you soon.",
            "data": {
                "name": contact.name,
                "email": contact.email,
                "subject": contact.subject
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contact form error: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Loan Prediction API",
        "version": "1.0.0"
    }