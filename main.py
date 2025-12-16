import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# NOTE: We do NOT import rag_engine here anymore.
# Importing it here would trigger the download immediately.

app = FastAPI(title="SHL Product Recommender API")

# Global variable to store the engine
engine = None

class QueryRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    # This endpoint will now be 100% instant.
    return {"status": "active", "message": "SHL RAG Tool is running."}

@app.post("/query")
def query_endpoint(request: QueryRequest):
    global engine
    
    # LAZY LOADING: Import and Load ONLY when needed.
    if engine is None:
        print("⚡️ First query detected. Importing & Loading AI Engine...")
        
        # 1. Scrape if needed
        if not os.path.exists('shl_products.json'):
            print("Data not found. Running ingestion...")
            try:
                from ingest import scrape_shl_catalog
                scrape_shl_catalog()
            except ImportError:
                print("Warning: ingest.py not found.")
        
        # 2. MOVING THE IMPORT HERE IS THE KEY FIX
        from rag_engine import SHLRecommendationEngine
        engine = SHLRecommendationEngine()
    
    if not engine:
        raise HTTPException(status_code=500, detail="Engine failed to initialize")
    
    result = engine.query(request.text)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)