# PDF to Embeddings Architecture Documentation

This directory contains architecture diagrams and documentation for the PDF to Embeddings system.

## Contents

1. [Architecture Overview](architecture.md)
   - System overview
   - Component diagram
   - Data flow
   - Dependencies

2. [Class Diagram](class_diagram.md)
   - Detailed class structure
   - Function call flow
   - Method descriptions

3. [Deployment Diagram](deployment_diagram.md)
   - Local deployment
   - Potential cloud deployment
   - Scaling considerations
   - Implementation roadmap

## How to View the Diagrams

The diagrams are written in Mermaid markdown format. You can view them in several ways:

1. **GitHub**: If you're viewing this on GitHub, the diagrams should render automatically.

2. **VS Code**: Install the "Markdown Preview Mermaid Support" extension to view the diagrams in VS Code's markdown preview.

3. **Mermaid Live Editor**: Copy the diagram code and paste it into the [Mermaid Live Editor](https://mermaid.live/) to view and edit the diagrams.

4. **Export to Images**: Use the Mermaid CLI or online tools to export the diagrams to PNG, SVG, or other formats.

## System Summary

The PDF to Embeddings system is designed to:

1. Extract text from PDF documents
2. Split the text into manageable chunks
3. Generate vector embeddings for each chunk using Hugging Face models
4. Store the embeddings in a Chroma vector database
5. Enable semantic search across the document collection

The system is currently implemented as a local CLI application but could be extended to a web service or cloud deployment as outlined in the deployment diagram.
