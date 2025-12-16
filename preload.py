from llama_index.embeddings.huggingface import HuggingFaceEmbedding

print("Starting Model Download during Build...")
HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
print(" Model Downloaded Successfully!")