from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingGenerator:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    def get_embeddings(self):
        return self.embedding_model
    