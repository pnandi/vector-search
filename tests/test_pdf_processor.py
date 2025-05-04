import os
import pytest
from pdf_to_embeddings import PDFProcessor
from PyPDF2 import PdfReader

@pytest.fixture
def test_pdf_path(tmp_path):
    # Create a test PDF file
    pdf_path = tmp_path / "test.pdf"
    with open(pdf_path, "w") as f:
        f.write("This is a test PDF content.")
    return str(pdf_path)

@pytest.fixture
def pdf_processor(tmp_path):
    # Create a PDF processor with temporary directories
    pdf_dir = tmp_path / "pdfs"
    persist_dir = tmp_path / "chroma_db"
    pdf_dir.mkdir()
    persist_dir.mkdir()
    return PDFProcessor(str(pdf_dir), str(persist_dir))

def test_extract_text_from_pdf(pdf_processor, test_pdf_path):
    # Test PDF text extraction
    text = pdf_processor.extract_text_from_pdf(test_pdf_path)
    assert isinstance(text, str)
    assert len(text) > 0

def test_process_pdfs(pdf_processor, test_pdf_path):
    # Test PDF processing
    # Copy test PDF to the processor's PDF directory
    import shutil
    shutil.copy(test_pdf_path, os.path.join(pdf_processor.pdf_directory, "test.pdf"))
    
    texts = pdf_processor.process_pdfs()
    assert isinstance(texts, list)
    assert len(texts) > 0
    assert all(isinstance(text, str) for text in texts)

def test_create_vector_store(pdf_processor, test_pdf_path):
    # Test vector store creation
    # Copy test PDF to the processor's PDF directory
    import shutil
    shutil.copy(test_pdf_path, os.path.join(pdf_processor.pdf_directory, "test.pdf"))
    
    texts = pdf_processor.process_pdfs()
    pdf_processor.create_vector_store(texts)
    
    assert pdf_processor.vector_store is not None
    assert os.path.exists(pdf_processor.persist_directory)

def test_search(pdf_processor, test_pdf_path):
    # Test search functionality
    # Copy test PDF to the processor's PDF directory
    import shutil
    shutil.copy(test_pdf_path, os.path.join(pdf_processor.pdf_directory, "test.pdf"))
    
    texts = pdf_processor.process_pdfs()
    pdf_processor.create_vector_store(texts)
    
    results = pdf_processor.search("test content")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, str) for result in results)

def test_invalid_search(pdf_processor):
    # Test search without initializing vector store
    with pytest.raises(ValueError):
        pdf_processor.search("test query")

def test_text_splitter_configuration(pdf_processor):
    # Test text splitter configuration
    assert pdf_processor.text_splitter._chunk_size == 1000
    assert pdf_processor.text_splitter._chunk_overlap == 200

def test_embeddings_configuration(pdf_processor):
    # Test embeddings configuration
    assert pdf_processor.embeddings.model_name == "sentence-transformers/all-MiniLM-L6-v2" 