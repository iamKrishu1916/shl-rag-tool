import os
import json
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

load_dotenv()

Settings.llm = Gemini(model="models/gemini-2.5-flash")

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

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