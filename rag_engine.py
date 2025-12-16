import os
import json
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext, load_index_from_storage
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
Settings.llm = Gemini(model="models/gemini-pro")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

class SHLRecommendationEngine:
    def __init__(self, data_file='shl_products.json', persist_dir="./storage"):
        # Check if we have a pre-calculated index on disk
        if os.path.exists(persist_dir):
            print(f"Found pre-built index in {persist_dir}. Loading...")
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            self.index = load_index_from_storage(storage_context)
        else:
            print("⚙️ No pre-built index found. Building from scratch (This is slow)...")
            self.index = self._build_index(data_file)
            # SAVE the index to disk so we never have to build it again
            print(f"Saving index to {persist_dir}...")
            self.index.storage_context.persist(persist_dir=persist_dir)
        
    def _build_index(self, data_file):
        if not os.path.exists(data_file):
            # If file is missing, just return empty list to prevent crash
            print(f"⚠️ Warning: {data_file} not found.")
            return VectorStoreIndex.from_documents([])
            
        with open(data_file, 'r') as f:
            data = json.load(f)
            
        documents = [
            Document(
                text=f"{item['title']}: {item['description']}",
                metadata={"title": item['title'], "category": item['category']}
            ) for item in data
        ]
        
        return VectorStoreIndex.from_documents(documents)

    def query(self, user_query):
        query_engine = self.index.as_query_engine(similarity_top_k=5)
        response = query_engine.query(f"Recommend a product for: '{user_query}'. Explain WHY.")
        
        return {
            "query": user_query,
            "response": str(response),
            "source_nodes": [n.node.metadata['title'] for n in response.source_nodes]
        }