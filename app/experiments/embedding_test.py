from app.embeddings.ollama import OllamaEmbedding

embedding = OllamaEmbedding()

text = "Hi!!!"

vector = embedding.embed(text)

print("Vector dimensions:", len(vector))
print("First 10 values", vector[:10])
