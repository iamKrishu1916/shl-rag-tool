import os
import json
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# 1. LLM: Use "models/gemini-pro".
# This is a generic alias that always points to the current stable model.
Settings.llm = Gemini(model="models/gemini-2.5-flash")

# 2. EMBEDDINGS: Use Local HuggingFace model.
# This runs on your CPU and avoids Google's rate limits.
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

class SHLRecommendationEngine:
    def __init__(self, data_file='shl_products.json'):
        self.index = self._build_index(data_file)
        
    def _build_index(self, data_file):
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"{data_file} not found. Run ingest.py first.")
            
        with open(data_file, 'r') as f:
            data = json.load(f)
            
        documents = [
            Document(
                text=f"{item['title']}: {item['description']}",
                metadata={"title": item['title'], "category": item['category']}
            ) for item in data
        ]
        
        print("indexing data locally (HuggingFace)...")
        # This will download the small model (~130MB) on the first run.
        return VectorStoreIndex.from_documents(documents)

    def query(self, user_query):
        query_engine = self.index.as_query_engine(similarity_top_k=5)
        
        response = query_engine.query(
            f"Recommend a product for: '{user_query}'. Explain WHY."
        )
        
        return {
            "query": user_query,
            "response": str(response),
            "source_nodes": [n.node.metadata['title'] for n in response.source_nodes]
        }