import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_engine import SHLRecommendationEngine
import uvicorn

app = FastAPI(title="SHL Product Recommender API")

# Global variable to store the engine, but we don't load it yet.
engine = None

class QueryRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    # This endpoint works instantly, proving to Render the app is alive.
    return {"status": "active", "message": "SHL RAG Tool is running."}

@app.post("/query")
def query_endpoint(request: QueryRequest):
    global engine
    
    # LAZY LOADING: Load the model only when the first user asks a question.
    if engine is None:
        print("⚡️ First query detected. Loading AI Engine... (This may take a moment)")
        
        # 1. Check if data exists, if not scrape it
        if not os.path.exists('shl_products.json'):
            print("Data not found. Running ingestion...")
            try:
                from ingest import scrape_shl_catalog
                scrape_shl_catalog()
            except ImportError:
                print("Warning: ingest.py not found.")
        
        # 2. Load the AI Engine (Downloads model if needed)
        engine = SHLRecommendationEngine()
    
    if not engine:
        raise HTTPException(status_code=500, detail="Engine failed to initialize")
    
    result = engine.query(request.text)
    return result

if __name__ == "__main__":
    # Local running command
    uvicorn.run(app, host="0.0.0.0", port=8000)