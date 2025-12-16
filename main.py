import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI(title="SHL Product Recommender API")

engine = None

class QueryRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "active", "message": "SHL RAG Tool is running."}

@app.post("/query")
def query_endpoint(request: QueryRequest):
    global engine
    
    if engine is None:
        print("⚡️ First query detected. Importing & Loading AI Engine...")
        
        if not os.path.exists('shl_products.json'):
            print("Data not found. Running ingestion...")
            try:
                from ingest import scrape_shl_catalog
                scrape_shl_catalog()
            except ImportError:
                print("Warning: ingest.py not found.")
        
        from rag_engine import SHLRecommendationEngine
        engine = SHLRecommendationEngine()
    
    if not engine:
        raise HTTPException(status_code=500, detail="Engine failed to initialize")
    
    result = engine.query(request.text)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)