# PDF to Embeddings Converter

This project provides a solution for converting PDF documents into vector embeddings and storing them in a vector database for efficient semantic search. It uses modern NLP techniques to process PDF documents and make them searchable using natural language queries.

## Features

- PDF text extraction
- Text chunking with configurable size and overlap
- Embedding generation using state-of-the-art language models
- Vector storage using ChromaDB
- Semantic search capabilities
- Persistent storage of vector embeddings

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd pdf-to-embeddings
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your PDF files in the `pdfs` directory

2. Run the main script:
```bash
python pdf_to_embeddings.py
```

3. For interactive search, use the execution script:
```bash
./run.sh
```

## Project Structure

```
.
├── pdfs/                  # Directory for PDF files
├── chroma_db/            # Directory for vector store persistence
├── tests/                # Unit tests
├── MCP/                  # Model Context Protocol integration
│   ├── mcp_server.py     # MCP server implementation
│   ├── llm_integration.py # LLM integration with MCP
│   ├── test_mcp_server.py # Test script for MCP server
│   ├── run_mcp.sh        # Script to run MCP server and tests
│   ├── mcp_requirements.txt # MCP-specific dependencies
│   └── README.md         # MCP integration documentation
├── pdf_to_embeddings.py  # Main processing script
├── run.sh                # Execution script
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Configuration

You can modify the following parameters in `pdf_to_embeddings.py`:
- `chunk_size`: Size of text chunks (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)
- `embedding_model`: The model used for generating embeddings (default: "sentence-transformers/all-MiniLM-L6-v2")

## Testing

Run the unit tests:
```bash
python -m pytest tests/
```

## License

MIT License

## MCP Integration

This project includes a Model Context Protocol (MCP) integration that allows you to connect your vector search system to Large Language Models (LLMs) for enhanced responses.

### What is MCP?

Model Context Protocol (MCP) is a standardized way for LLMs to request and receive additional context from external knowledge sources. By implementing an MCP server for your vector search system, you can:

1. Provide LLMs with relevant document snippets from your PDF collection
2. Ground LLM responses in your specific documents, reducing hallucinations
3. Get more accurate and relevant answers based on your document collection

### Using the MCP Integration

To use the MCP integration:

1. Make sure your vector store is initialized by running the main script:
   ```bash
   python pdf_to_embeddings.py
   ```

2. Navigate to the MCP directory:
   ```bash
   cd MCP
   ```

3. Install the MCP-specific dependencies:
   ```bash
   pip install -r mcp_requirements.txt
   ```

4. Run the MCP server and test script:
   ```bash
   ./run_mcp.sh
   ```

For more detailed information, see the [MCP README](MCP/README.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.