# PDF to Embeddings Class Diagram

This document provides a detailed class diagram and function call flow for the PDF to Embeddings system.

## Class Diagram

```mermaid
classDiagram
    class PDFProcessor {
        -pdf_directory: str
        -persist_directory: str
        -text_splitter: RecursiveCharacterTextSplitter
        -embeddings: HuggingFaceEmbeddings
        -vector_store: Chroma
        +__init__(pdf_directory: str, persist_directory: str)
        +extract_text_from_pdf(pdf_path: str) -> str
        +process_pdfs() -> List[str]
        +create_vector_store(texts: List[str])
        +search(query: str, k: int) -> List[str]
    }
    
    class RecursiveCharacterTextSplitter {
        -chunk_size: int
        -chunk_overlap: int
        -length_function: function
        +split_text(text: str) -> List[str]
    }
    
    class HuggingFaceEmbeddings {
        -model_name: str
        +embed_documents(texts: List[str]) -> List[List[float]]
        +embed_query(text: str) -> List[float]
    }
    
    class Chroma {
        -persist_directory: str
        -embedding_function: HuggingFaceEmbeddings
        +from_texts(texts: List[str], embedding: HuggingFaceEmbeddings, persist_directory: str) -> Chroma
        +persist()
        +similarity_search(query: str, k: int) -> List[Document]
    }
    
    class PdfReader {
        -pages: List[PageObject]
        +__init__(pdf_path: str)
    }
    
    class PageObject {
        +extract_text() -> str
    }
    
    PDFProcessor --> RecursiveCharacterTextSplitter : uses
    PDFProcessor --> HuggingFaceEmbeddings : uses
    PDFProcessor --> Chroma : uses
    PDFProcessor --> PdfReader : uses
    PdfReader --> PageObject : contains
```

## Function Call Flow

```mermaid
sequenceDiagram
    participant User
    participant run.sh
    participant PDFProcessor
    participant PyPDF2
    participant TextSplitter
    participant HuggingFaceEmbeddings
    participant Chroma
    
    %% PDF Processing Flow
    User->>run.sh: Select "Process PDFs"
    run.sh->>PDFProcessor: main()
    PDFProcessor->>PDFProcessor: process_pdfs()
    loop For each PDF file
        PDFProcessor->>PyPDF2: PdfReader(pdf_path)
        PyPDF2->>PDFProcessor: reader
        loop For each page
            PDFProcessor->>PyPDF2: page.extract_text()
            PyPDF2->>PDFProcessor: text
        end
        PDFProcessor->>TextSplitter: split_text(text)
        TextSplitter->>PDFProcessor: chunks
    end
    PDFProcessor->>PDFProcessor: create_vector_store(texts)
    PDFProcessor->>HuggingFaceEmbeddings: embed_documents(texts)
    HuggingFaceEmbeddings->>PDFProcessor: embeddings
    PDFProcessor->>Chroma: from_texts(texts, embeddings, persist_directory)
    Chroma->>PDFProcessor: vector_store
    PDFProcessor->>Chroma: persist()
    
    %% Search Flow
    User->>run.sh: Select "Search" and enter query
    run.sh->>PDFProcessor: Initialize
    run.sh->>HuggingFaceEmbeddings: Initialize
    run.sh->>Chroma: Initialize with persist_directory
    run.sh->>PDFProcessor: Set vector_store
    run.sh->>PDFProcessor: search(query)
    PDFProcessor->>HuggingFaceEmbeddings: embed_query(query)
    HuggingFaceEmbeddings->>PDFProcessor: query_embedding
    PDFProcessor->>Chroma: similarity_search(query, k)
    Chroma->>PDFProcessor: documents
    PDFProcessor->>run.sh: results
    run.sh->>User: Display results
```

## Function Details

### PDFProcessor Class

#### `__init__(pdf_directory: str, persist_directory: str = "chroma_db")`
- **Purpose**: Initialize the PDFProcessor with directories and components
- **Parameters**:
  - `pdf_directory`: Directory containing PDF files
  - `persist_directory`: Directory for storing vector database
- **Actions**:
  - Sets up the text splitter with chunk_size=1000, chunk_overlap=200
  - Initializes HuggingFaceEmbeddings with model "sentence-transformers/all-MiniLM-L6-v2"
  - Sets vector_store to None initially

#### `extract_text_from_pdf(pdf_path: str) -> str`
- **Purpose**: Extract text from a single PDF file
- **Parameters**:
  - `pdf_path`: Path to the PDF file
- **Returns**: Extracted text as a string
- **Actions**:
  - Creates a PdfReader for the file
  - Iterates through pages and extracts text
  - Concatenates all page texts

#### `process_pdfs() -> List[str]`
- **Purpose**: Process all PDFs in the directory
- **Returns**: List of text chunks
- **Actions**:
  - Scans the PDF directory for PDF files
  - For each PDF, extracts text and splits into chunks
  - Collects all chunks into a list

#### `create_vector_store(texts: List[str])`
- **Purpose**: Create and persist the vector store
- **Parameters**:
  - `texts`: List of text chunks to embed
- **Actions**:
  - Creates a Chroma vector store from texts
  - Persists the vector store to disk

#### `search(query: str, k: int = 3) -> List[str]`
- **Purpose**: Search the vector store for similar content
- **Parameters**:
  - `query`: Search query
  - `k`: Number of results to return
- **Returns**: List of text chunks matching the query
- **Actions**:
  - Checks if vector_store is initialized
  - Performs similarity search
  - Extracts and returns page content from results
