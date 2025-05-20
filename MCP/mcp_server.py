"""
MCP Server Adapter for PDF to Embeddings Vector Search

This module implements a Model Context Protocol (MCP) server that connects
the PDF to Embeddings vector search system to LLMs, providing relevant
document context for improved responses.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import sys
import os

# Add the parent directory to the path so we can import the main project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_to_embeddings import PDFProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Vector Search MCP Server",
    description="Model Context Protocol server for PDF to Embeddings vector search",
    version="0.1.0"
)

# Initialize the PDF processor with the existing setup
# Use paths relative to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_dir = os.path.join(parent_dir, "pdfs")
chroma_dir = os.path.join(parent_dir, "chroma_db")
processor = PDFProcessor(pdf_directory=pdf_dir, persist_directory=chroma_dir)

class MCPRequest(BaseModel):
    """Model Context Protocol request schema"""
    query: str
    max_tokens: Optional[int] = 1000
    threshold: Optional[float] = 0.7
    top_k: Optional[int] = 5

class MCPResponse(BaseModel):
    """Model Context Protocol response schema"""
    contexts: List[Dict[str, Any]]
    metadata: Dict[str, Any] = {}

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"status": "healthy", "service": "Vector Search MCP Server"}

@app.post("/context", response_model=MCPResponse)
async def get_context(request: MCPRequest):
    """
    Provide context from vector search for an LLM query

    This endpoint accepts a query and returns relevant document contexts
    from the PDF to Embeddings vector search system.
    """
    logger.info(f"Received context request: {request.query}")

    try:
        # Use the existing search functionality
        k = request.top_k if request.top_k else 5
        results = processor.search(request.query, k=k)

        logger.info(f"Found {len(results)} results for query: {request.query}")

        # Format results according to MCP specification
        contexts = []
        for i, result in enumerate(results):
            # Calculate a simple relevance score that decreases with rank
            relevance_score = max(0.5, 1.0 - (i * 0.1))

            contexts.append({
                "content": result,
                "relevance_score": relevance_score,
                "source": "pdf_embeddings",
                "rank": i + 1
            })

        # Return the formatted response
        return MCPResponse(
            contexts=contexts,
            metadata={
                "total_results": len(results),
                "source": "PDF to Embeddings Vector Search",
                "query": request.query
            }
        )
    except ValueError as e:
        # Handle the case where vector store is not initialized
        logger.error(f"Vector store error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle other exceptions
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if the vector store is initialized by attempting a simple search
        # This will raise a ValueError if the vector store is not initialized
        processor.search("test", k=1)
        return {"status": "healthy", "vector_store": "initialized"}
    except ValueError:
        # Return a 200 status but indicate that the vector store is not initialized
        return {"status": "partially_healthy", "vector_store": "not_initialized"}
    except Exception as e:
        # Return a 500 status for other errors
        raise HTTPException(status_code=500, detail=str(e))

def start_server(host="0.0.0.0", port=8080):
    """Start the MCP server"""
    uvicorn.run("mcp_server:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    start_server()
