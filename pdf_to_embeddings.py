import os
from typing import List
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PDFProcessor:
    def __init__(self, pdf_directory: str, persist_directory: str = "chroma_db"):
        self.pdf_directory = pdf_directory
        self.persist_directory = persist_directory
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a single PDF file."""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def process_pdfs(self) -> List[str]:
        """Process all PDFs in the directory and return chunks of text."""
        all_texts = []
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(self.pdf_directory, filename)
                print(f"Processing {filename}...")
                text = self.extract_text_from_pdf(pdf_path)
                texts = self.text_splitter.split_text(text)
                all_texts.extend(texts)
        return all_texts

    def create_vector_store(self, texts: List[str]):
        """Create and persist the vector store."""
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.vector_store.persist()
        print(f"Vector store created and persisted to {self.persist_directory}")

    def search(self, query: str, k: int = 3) -> List[str]:
        """Search the vector store for similar content."""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please process PDFs first.")
        
        docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

def main():
    # Example usage
    pdf_dir = "pdfs"  # Directory containing PDF files
    processor = PDFProcessor(pdf_directory=pdf_dir)
    
    # Process PDFs and create vector store
    texts = processor.process_pdfs()
    processor.create_vector_store(texts)
    
    # Example search
    query = "What is the main topic of the documents?"
    results = processor.search(query)
    print("\nSearch results:")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(result)

if __name__ == "__main__":
    main() 