"""
LLM Integration with MCP Server

This script demonstrates how to integrate an LLM with the MCP server
to provide context-enhanced responses based on the PDF to Embeddings vector search.
"""

import os
import requests
import argparse
import logging
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv
import openai

# Add the parent directory to the path if needed
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class MCPClient:
    """Client for interacting with the MCP server"""

    def __init__(self, server_url: str = "http://localhost:8080"):
        """
        Initialize the MCP client

        Args:
            server_url: URL of the MCP server
        """
        self.server_url = server_url
        self.context_endpoint = f"{server_url}/context"

    def get_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Get context from the MCP server for a query

        Args:
            query: The query to get context for
            top_k: Number of context items to retrieve

        Returns:
            List of context items
        """
        try:
            response = requests.post(
                self.context_endpoint,
                json={
                    "query": query,
                    "top_k": top_k
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data["contexts"]
            else:
                logger.error(f"Error from MCP server: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error connecting to MCP server: {str(e)}")
            return []

def query_llm(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Query an LLM with a prompt

    Args:
        prompt: The prompt to send to the LLM
        model: The model to use

    Returns:
        The LLM's response
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides accurate information based on the context provided."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error querying LLM: {str(e)}")
        return f"Error: {str(e)}"

def generate_context_enhanced_prompt(query: str, contexts: List[Dict[str, Any]]) -> str:
    """
    Generate a prompt enhanced with context for the LLM

    Args:
        query: The user's query
        contexts: Context items from the MCP server

    Returns:
        A prompt with context for the LLM
    """
    prompt = f"Question: {query}\n\n"

    if contexts:
        prompt += "Context information:\n"
        for i, context in enumerate(contexts):
            prompt += f"\n--- Context {i+1} ---\n{context['content']}\n"

        prompt += "\nBased on the context information provided above, please answer the question. If the context doesn't contain relevant information to answer the question, please say so."
    else:
        prompt += "No context information available. Please answer based on your knowledge."

    return prompt

def main():
    """Main function to run the LLM integration"""
    parser = argparse.ArgumentParser(description="LLM Integration with MCP Server")
    parser.add_argument("--query", type=str, help="Query to send to the LLM")
    parser.add_argument("--server", type=str, default="http://localhost:8080", help="MCP server URL")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="LLM model to use")
    parser.add_argument("--top_k", type=int, default=3, help="Number of context items to retrieve")

    args = parser.parse_args()

    # If no query is provided, use interactive mode
    if not args.query:
        print("Enter 'exit' to quit")
        while True:
            query = input("\nEnter your query: ")
            if query.lower() == 'exit':
                break
            process_query(query, args.server, args.model, args.top_k)
    else:
        process_query(args.query, args.server, args.model, args.top_k)

def process_query(query: str, server_url: str, model: str, top_k: int):
    """
    Process a query using the MCP server and LLM

    Args:
        query: The query to process
        server_url: URL of the MCP server
        model: LLM model to use
        top_k: Number of context items to retrieve
    """
    logger.info(f"Processing query: {query}")

    # Get context from MCP server
    mcp_client = MCPClient(server_url)
    contexts = mcp_client.get_context(query, top_k)

    if contexts:
        logger.info(f"Retrieved {len(contexts)} context items")
    else:
        logger.warning("No context retrieved from MCP server")

    # Generate enhanced prompt with context
    prompt = generate_context_enhanced_prompt(query, contexts)

    # Query the LLM
    logger.info(f"Querying LLM with model: {model}")
    response = query_llm(prompt, model)

    # Print the response
    print("\n--- LLM Response ---")
    print(response)
    print("\n--- Context Sources ---")
    if contexts:
        for i, context in enumerate(contexts):
            print(f"Context {i+1}: Relevance score {context['relevance_score']:.2f}")
    else:
        print("No context sources available")

if __name__ == "__main__":
    main()
