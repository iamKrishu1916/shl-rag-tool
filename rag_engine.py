from dotenv import load_dotenv
load_dotenv() 

import os
import json
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.postprocessor import LLMRerank

Settings.llm = OpenAI(model="gpt-4o", temperature=0.2)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

class SHLRecommendationEngine:
    def __init__(self, data_file='shl_products.json'):
        self.index = self._build_index(data_file)
        
    def _build_index(self, data_file):
        """Loads JSON data and builds a Vector Index."""
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
        
        print("indexing data...")
        return VectorStoreIndex.from_documents(documents)

    def query(self, user_query):
        """
        Modern RAG Technique:
        1. Retrieve top 5 nodes via Vector Search.
        2. Rerank nodes using the LLM to filter out irrelevant noise.
        """
        reranker = LLMRerank(choice_batch_size=5, top_n=3)
        
        query_engine = self.index.as_query_engine(
            similarity_top_k=5,
            node_postprocessors=[reranker],
            response_mode="compact" 
        )
        
        response = query_engine.query(
            f"You are an expert SHL consultant. Recommend a product based on this request: '{user_query}'. "
            "Explain WHY you chose it."
        )
        
        return {
            "query": user_query,
            "response": str(response),
            "source_nodes": [n.node.metadata['title'] for n in response.source_nodes]
        }