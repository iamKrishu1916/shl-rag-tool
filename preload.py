import os
from rag_engine import SHLRecommendationEngine

print("Starting Build-Time Preparation...")

if not os.path.exists("shl_products.json"):
    print("⚠️ Data file not found! Indexing might be empty.")

print("⚙️ Building and Saving Vector Index...")
SHLRecommendationEngine()

print("Index pre-built and saved to ./storage!")