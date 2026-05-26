import os

from app.ingestion.pdf_loader import PDFLoader

class DocumentIngestor:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_documents(self):
        all_documents = []

        for filename in os.listdir(self.data_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(self.data_path, filename)
                pdf_loader = PDFLoader(file_path)
                documents = pdf_loader.load_documents()
                all_documents.extend(documents)

        return all_documents