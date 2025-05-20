"""
Test script for the MCP server

This script tests the MCP server by sending requests and displaying the responses.
It doesn't require an OpenAI API key as it only tests the context retrieval part.
"""

import requests
import json
import argparse
import logging
import os
import sys
from typing import Dict, Any

# Add the parent directory to the path if needed
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_health(server_url: str) -> Dict[str, Any]:
    """
    Test the health endpoint

    Args:
        server_url: URL of the MCP server

    Returns:
        Response from the health endpoint
    """
    try:
        response = requests.get(f"{server_url}/health")
        return response.json()
    except Exception as e:
        logger.error(f"Error testing health endpoint: {str(e)}")
        return {"error": str(e)}

def test_context(server_url: str, query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Test the context endpoint

    Args:
        server_url: URL of the MCP server
        query: Query to send
        top_k: Number of results to request

    Returns:
        Response from the context endpoint
    """
    try:
        response = requests.post(
            f"{server_url}/context",
            json={
                "query": query,
                "top_k": top_k
            }
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error testing context endpoint: {str(e)}")
        return {"error": str(e)}

def main():
    """Main function to run the tests"""
    parser = argparse.ArgumentParser(description="Test the MCP server")
    parser.add_argument("--server", type=str, default="http://localhost:8080", help="MCP server URL")
    parser.add_argument("--query", type=str, default="menstrual bleeding", help="Query to test")
    parser.add_argument("--top_k", type=int, default=3, help="Number of results to request")

    args = parser.parse_args()

    # Test the health endpoint
    logger.info("Testing health endpoint...")
    health_response = test_health(args.server)
    print("\n--- Health Check Response ---")
    print(json.dumps(health_response, indent=2))

    # Test the context endpoint
    logger.info(f"Testing context endpoint with query: {args.query}")
    context_response = test_context(args.server, args.query, args.top_k)
    print("\n--- Context Response ---")
    print(json.dumps(context_response, indent=2))

    # Print the actual context content
    if "contexts" in context_response and context_response["contexts"]:
        print("\n--- Retrieved Contexts ---")
        for i, context in enumerate(context_response["contexts"]):
            print(f"\nContext {i+1} (Relevance: {context.get('relevance_score', 'N/A')}):")
            print(context.get("content", "No content available"))
    else:
        print("\nNo contexts retrieved or error in response")

if __name__ == "__main__":
    main()
