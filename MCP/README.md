# MCP Server for PDF to Embeddings Vector Search

This extension adds Model Context Protocol (MCP) server capabilities to the PDF to Embeddings vector search project, allowing you to connect your document search to Large Language Models (LLMs) for enhanced responses.

## What is MCP?

Model Context Protocol (MCP) is a standardized way for LLMs to request and receive additional context from external knowledge sources. By implementing an MCP server for your vector search system, you can:

1. Provide LLMs with relevant document snippets from your PDF collection
2. Ground LLM responses in your specific documents, reducing hallucinations
3. Get more accurate and relevant answers based on your document collection

## Components

This integration consists of two main components:

1. **MCP Server (`mcp_server.py`)**: A FastAPI server that exposes your vector search system via the MCP protocol
2. **LLM Integration (`llm_integration.py`)**: A client script that demonstrates how to use the MCP server with an LLM

## Setup

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key (for the LLM integration)
- Your PDF to Embeddings project already set up and working

### Installation

1. Install the required dependencies:

```bash
pip install -r mcp_requirements.txt
```

2. Configure your OpenAI API key in the `.env` file:

```bash
# Edit the .env file
OPENAI_API_KEY=your_openai_api_key_here
```

### Starting the MCP Server

1. Make sure your vector database is already populated by running your PDF processing script:

```bash
python pdf_to_embeddings.py
```

2. Start the MCP server:

```bash
python mcp_server.py
```

The server will start on http://localhost:8080 by default.

### Testing with the LLM Integration

Once the MCP server is running, you can test it with the LLM integration script:

```bash
# Interactive mode
python llm_integration.py

# Or with a specific query
python llm_integration.py --query "What is mentioned about menstrual bleeding in the documents?"
```

## API Endpoints

The MCP server exposes the following endpoints:

- `GET /`: Health check endpoint
- `GET /health`: Detailed health check that verifies vector store initialization
- `POST /context`: Main MCP endpoint that provides context for queries

### Context Endpoint

The `/context` endpoint accepts POST requests with the following JSON structure:

```json
{
  "query": "Your search query here",
  "max_tokens": 1000,
  "threshold": 0.7,
  "top_k": 5
}
```

And returns responses in this format:

```json
{
  "contexts": [
    {
      "content": "Text content from the document",
      "relevance_score": 0.95,
      "source": "pdf_embeddings",
      "rank": 1
    },
    ...
  ],
  "metadata": {
    "total_results": 5,
    "source": "PDF to Embeddings Vector Search",
    "query": "Your search query here"
  }
}
```

## Customization

### Changing the Server Port

You can change the server port by modifying the `.env` file or by passing arguments to the `start_server` function:

```python
# In mcp_server.py
if __name__ == "__main__":
    start_server(host="0.0.0.0", port=9000)
```

### Using a Different LLM Provider

The LLM integration script currently uses OpenAI's API, but you can modify it to use any LLM provider by changing the `query_llm` function in `llm_integration.py`.

## Troubleshooting

### Vector Store Not Initialized

If you see an error like "Vector store not initialized. Please process PDFs first.", make sure you've run your PDF processing script before starting the MCP server:

```bash
python pdf_to_embeddings.py
```

### Connection Refused

If you see a "Connection refused" error when running the LLM integration script, make sure the MCP server is running and accessible at the specified URL.

## Next Steps

1. **Add Authentication**: For production use, add authentication to your MCP server
2. **Implement Caching**: Add caching to improve performance for repeated queries
3. **Enhance Context Processing**: Improve context selection and formatting for better LLM responses
4. **Add Streaming Support**: Implement streaming responses for better user experience
5. **Deploy to Production**: Set up proper deployment with monitoring and scaling
