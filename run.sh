#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p pdfs
mkdir -p chroma_db

# Function to process PDFs
process_pdfs() {
    echo "Processing PDFs..."
    python pdf_to_embeddings.py
}

# Function to perform search
search() {
    read -p "Enter your search query: " query
    python -c "
from pdf_to_embeddings import PDFProcessor
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Initialize the processor with the same embeddings model
processor = PDFProcessor(pdf_directory='pdfs', persist_directory='chroma_db')

# Load the existing vector store
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
processor.vector_store = Chroma(persist_directory='chroma_db', embedding_function=embeddings)

# Perform the search
results = processor.search('$query')
print('\nSearch results:')
for i, result in enumerate(results, 1):
    print(f'\nResult {i}:')
    print(result)
"
}

# Main menu
while true; do
    echo -e "\nPDF to Embeddings Converter"
    echo "1. Process PDFs"
    echo "2. Search"
    echo "3. Exit"
    read -p "Choose an option (1-3): " choice

    case $choice in
        1)
            process_pdfs
            ;;
        2)
            search
            ;;
        3)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
done