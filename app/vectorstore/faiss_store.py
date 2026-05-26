import os

from langchain_community.vectorstores import FAISS


class VectorStoreManager:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

        self.index_path = "storage/faiss_index"

    def create_vector_store(self, chunks):

        vector_store = FAISS.from_documents(
            chunks,
            self.embedding_model
        )

        vector_store.save_local(self.index_path)

        return vector_store

    def load_vector_store(self):
        faiss_file = os.path.join(
        self.index_path,
        "index.faiss"
        )

        pkl_file = os.path.join(
        self.index_path,
        "index.pkl"
        )


        if not os.path.exists(faiss_file) or not os.path.exists(pkl_file):
            

            return None

        vector_store = FAISS.load_local(
            self.index_path,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        return vector_store
    