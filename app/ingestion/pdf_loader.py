from langchain_community.document_loaders import PyPDFLoader

class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_documents(self):
        loader = PyPDFLoader(self.file_path)
        documents = loader.load()
        return documents