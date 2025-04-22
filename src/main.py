"""
AgroFlow Backend API

This module provides API endpoints for plant disease prediction and document search.
"""
# Standard library imports
import os
import pickle
from typing import Dict, List, Optional, Union

# Third-party imports
from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from mistralai import Mistral
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Local application imports
from plant_disease.disease_prediction import predict_from_image


# Client initialization
def initialize_qdrant() -> QdrantClient:
    """
    Initialize Qdrant vector database client and load document embeddings.
    
    Returns:
        QdrantClient: Initialized Qdrant client
    """
    # Create Qdrant client - using :memory: for testing, but in production should use a persistent storage
    qdrant_client = QdrantClient(":memory:")
    
    # Load document embeddings if the pickle file exists
    embeddings_file = os.path.join("RAG", "document_embeddings.pkl")
    if os.path.exists(embeddings_file):
        try:
            with open(embeddings_file, "rb") as f:
                document_embeddings = pickle.load(f)
                
            # Create collections for different document types if they don't exist
            collection_name = "technical_reports"
            # Check if collection exists
            try:
                qdrant_client.get_collection(collection_name=collection_name)
            except Exception:
                # Create collection if it doesn't exist
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
                )
            
            # Process tabular structured embeddings and create points for Qdrant
            collection_points = []
            
            # Format of embeddings_file: id  vector  payload
            # Where id column contains UUIDs that should be used as Qdrant IDs
            for _, row in document_embeddings.iterrows():
                try:
                    # Extract UUID from the id column to use as the actual Qdrant ID
                    point_id = row['id']
                    vector = row['vector']
                    payload = row['payload']
                    
                    collection_points.append(
                        PointStruct(
                            id=point_id,
                            vector=vector,
                            payload=payload
                        )
                    )
                except Exception as e:
                    print(f"Error processing embedding row: {e}")
                    continue
                
                # Only upsert if there are points for this collection
                if collection_points:
                    qdrant_client.upsert(
                        collection_name=collection_name,
                        points=collection_points
                    )

            print(f"Loaded {len(collection_points)} document embeddings for {collection_name}")
            print("Document embeddings loaded successfully")
            
        except Exception as e:
            print(f"Error loading document embeddings: {str(e)}")
    else:
        print(f"Document embeddings file not found at {embeddings_file}")
    
    return qdrant_client


def initialize_mistral() -> Optional[Mistral]:
    """
    Initialize Mistral AI client for embeddings.
    
    Returns:
        Optional[Mistral]: Initialized Mistral client or None if API key is not available
    """
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    if mistral_api_key:
        return Mistral(api_key=mistral_api_key)
    else:
        print("Warning: MISTRAL_API_KEY environment variable not set")
        return None


# Initialize clients
qdrant_client = initialize_qdrant()
mistral_client = initialize_mistral()

# Initialize FastAPI app
app = FastAPI(
    title="AgroFlow backend",
    description="API for helping farmers with plant disease prediction and document search",
    version="1.0.0"
)

# Make the clients accessible to API endpoints
app.state.qdrant_client = qdrant_client
app.state.mistral_client = mistral_client


# API Routes
@app.get("/")
async def root() -> Dict[str, Union[str, List[str]]]:
    """Root endpoint providing API information."""
    return {
        "message": "Plant Disease Prediction API",
        "docs": "/docs",
        "endpoints": [
            "/predict/upload - Upload an image file for prediction",
            "/search - Search document embeddings",
            "/health - API health check"
        ]
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """API health check endpoint."""
    return {"status": "healthy"}


@app.post("/predict/upload")
async def predict_image(file: UploadFile = File(...)) -> Dict:
    """
    Predict plant disease from an uploaded image file.
    
    Args:
        file: Image file to analyze
    
    Returns:
        Prediction results with confidence scores
    
    Raises:
        HTTPException: If file is not an image or prediction fails
    """
    # Validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read file content
        contents = await file.read()
        
        # Make prediction
        results = predict_from_image(image_data=contents)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/search")
async def search_documents(
    query: str, 
    collection: str = "technical_reports", 
    limit: int = 5
) -> Dict:
    """
    Search document embeddings using semantic similarity.
    
    Args:
        query: Text query to search for
        collection: Name of the collection to search in
        limit: Maximum number of results to return
    
    Returns:
        List of document chunks matching the query
    
    Raises:
        HTTPException: If search fails or Mistral client is not available
    """
    try:
        mistral_client = app.state.mistral_client
        if not mistral_client:
            raise HTTPException(status_code=500, detail="Mistral client not initialized")
        
        # Generate embedding for the query
        embedding_response = mistral_client.embeddings.create(
            model="mistral-embed",
            inputs=[query]
        )
        query_embedding = embedding_response.data[0].embedding
        
        # Search in Qdrant
        search_results = app.state.qdrant_client.search(
            collection_name=collection,
            query_vector=query_embedding,
            limit=limit
        )
        
        # Format results
        results = []
        for result in search_results:
            results.append({
                "text": result.payload.get("text", ""),
                "file_name": result.payload.get("file_name", ""),
                "date": result.payload.get("date", ""),
                "score": result.score
            })
        
        return {"results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
