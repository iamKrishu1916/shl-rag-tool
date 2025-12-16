import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_engine import SHLRecommendationEngine
import uvicorn

app = FastAPI(title="SHL Product Recommender API")
engine = None

class QueryRequest(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    global engine
    if not os.path.exists('shl_products.json'):
        from ingest import scrape_shl_catalog
        scrape_shl_catalog()
    engine = SHLRecommendationEngine()

@app.get("/")
def read_root():
    return {"status": "active", "message": "SHL RAG Tool is running. Query via /query endpoint."}

@app.post("/query")
def query_endpoint(request: QueryRequest):
    """
    API Endpoint: Accepts a text query and returns JSON result.
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    result = engine.query(request.text)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)