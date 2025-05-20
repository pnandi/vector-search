#!/bin/bash

# Run MCP Server and Test Script
# This script starts the MCP server and runs the test script

# Change to the MCP directory
cd "$(dirname "$0")"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python; then
    echo -e "${RED}Error: Python is not installed.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command_exists pip; then
    echo -e "${RED}Error: pip is not installed.${NC}"
    exit 1
fi

# Install dependencies if needed
echo -e "${YELLOW}Checking and installing dependencies...${NC}"
pip install -r mcp_requirements.txt

# Check if the vector store exists
if [ ! -d "../chroma_db" ]; then
    echo -e "${YELLOW}Warning: Vector store directory '../chroma_db' not found.${NC}"
    echo -e "${YELLOW}You may need to run 'python ../pdf_to_embeddings.py' first.${NC}"

    read -p "Do you want to run pdf_to_embeddings.py now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Running pdf_to_embeddings.py...${NC}"
        cd ..
        python pdf_to_embeddings.py
        cd - > /dev/null
    else
        echo -e "${YELLOW}Continuing without initializing vector store...${NC}"
    fi
fi

# Start the MCP server in the background
echo -e "${GREEN}Starting MCP server...${NC}"
python mcp_server.py &
SERVER_PID=$!

# Wait for the server to start
echo -e "${YELLOW}Waiting for server to start...${NC}"
sleep 5

# Run the test script
echo -e "${GREEN}Running test script...${NC}"
python test_mcp_server.py

# Ask if the user wants to run the LLM integration
echo
read -p "Do you want to run the LLM integration with OpenAI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if OPENAI_API_KEY is set in .env
    if grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
        echo -e "${YELLOW}Warning: OpenAI API key not set in .env file.${NC}"
        read -p "Enter your OpenAI API key: " API_KEY
        sed -i "s/OPENAI_API_KEY=your_openai_api_key_here/OPENAI_API_KEY=$API_KEY/" .env
    fi

    echo -e "${GREEN}Running LLM integration...${NC}"
    python llm_integration.py
fi

# Clean up
echo -e "${GREEN}Stopping MCP server...${NC}"
kill $SERVER_PID

echo -e "${GREEN}Done!${NC}"
