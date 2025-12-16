from llama_index.embeddings.huggingface import HuggingFaceEmbedding

print("⬇️ Starting Model Download during Build...")
# This triggers the download to the system cache
HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
print("✅ Model Downloaded Successfully!")