"""
Plant Disease Prediction API
Example FastAPI application using the disease_prediction module
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from plant_disease.disease_prediction import predict_from_image

# Create FastAPI app
app = FastAPI(
    title="Plant Disease Prediction API",
    description="API for predicting plant diseases from images",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Plant Disease Prediction API",
        "docs": "/docs",
        "endpoints": [
            "/predict/upload - Upload an image file for prediction",
            "/health - API health check"
        ]
    }

@app.post("/predict/upload")
async def predict_image(file: UploadFile = File(...)):
    """
    Predict plant disease from an uploaded image file
    
    Args:
        file: Image file to analyze
    
    Returns:
        Prediction results with confidence scores
    """
    # Validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read file content
        contents = await file.read()
        
        # Make prediction
        results = predict_from_image(
            image_data=contents,
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("fastapi_example:app", host="0.0.0.0", port=8000, reload=True)
