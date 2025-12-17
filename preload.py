import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from rag_engine import SHLRecommendationEngine

print("Starting Build-Time Preparation...")

# 1. EXPLICITLY download the model to a local project folder
# This ensures Render keeps the files after the build finishes.
print("Downloading Embedding Model to ./model_cache...")
HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./model_cache"
)
print("Model downloaded successfully!")

# 2. Build the Index
if not os.path.exists("shl_products.json"):
    print("⚠️ Data file not found! Indexing might be empty.")

print("⚙️ Building and Saving Vector Index...")
# This will now use the model we just downloaded into ./model_cache
SHLRecommendationEngine()

print("Index pre-built and saved to ./storage!")