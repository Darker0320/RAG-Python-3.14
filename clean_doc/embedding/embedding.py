from langchain_ollama import OllamaEmbeddings
# Use BGE-M3 model for embeddings
embeddings = OllamaEmbeddings(model = "bge-m3",base_url = "http://localhost:11434")

def do_embedding(enhanced_content:str)->list[float]:
    return embeddings.embed_query(enhanced_content)

