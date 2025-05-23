# Ennchan RAG Proof of Concept

A locally hosted chatbot that answers questions using internet search results.

## Project Overview

### What is this?
This is a Q&A chatbot that receives user questions, searches the internet for answers, and provides summarized responses. The project aims to create a local, self-hosted chatbot solution that runs directly on your PC.

### Why build it?
Traditional cloud-based solutions like ChatGPT and DeepSeek often face usage limits and server congestion. This project provides a local alternative that maintains high-quality responses while giving users full control over the models and search capabilities.

## Features

### Core Functionality
- Local-first architecture for independence from cloud services
- Flexible Q&A chatbot interface
- Pluggable model architecture supporting multiple LLMs
- Configurable search engine integration

### Query Capabilities
Users can ask any type of question, with response quality depending on:
- The loaded language model's capabilities
- Search engine result quality
- Available context window size
- Retrieval strategy effectiveness

### Technical Architecture

#### Search and Retrieval Pipeline
1. Query Processing
   - User input is processed and optimized for search
   - Query expansion techniques improve search relevance

2. Search Integration
   - Configurable search engine API integration (currently supports Brave Search)
   - Robust error handling and retry mechanisms
   - Asynchronous request handling for better performance

3. Information Retrieval
   - Multiple retrieval strategies available:
     - Semantic similarity matching
     - Keyword-based filtering
     - Hybrid approaches combining multiple methods
   - Context window optimization for model input

4. Response Generation
   - LLM-based summarization and answer synthesis
   - Source attribution and confidence scoring
   - Response quality filters

## Optimizations

### Performance Enhancements
- Multiprocessing for parallel search and processing
- Network request batching and retry mechanisms
- Efficient context window management
- Caching layer for frequently accessed data

### Resource Management
- Configurable batch sizes for processing
- Memory-efficient data structures
- Stream processing for large result sets

## Installation

```bash
pip install ennchan-search-*.whl  # Best done in a virtual environment
```

## Configuration

Create a config.json file:
```json
{
    "BRAVE_API_KEY": "your_api_key_here"
}
```

## Usage

### Basic Example
```python
from ennchan_search import search

config = "path/to/config.json"
query = "Ennchan"
answers = ask(query, config)
```

### Advanced Configuration
- Model selection and parameters
- Search engine preferences
- Retrieval strategy customization
- Response format options

## Interfaces

### Current
- Command Line Interface (CLI)

### Planned
- Web API (Coming Soon)
  - RESTful endpoints
  - WebSocket support for streaming responses
  - API documentation

## Future Development
- Additional search engine integrations
- Enhanced retrieval strategies
- Web interface
- Model fine-tuning capabilities
- Improved caching mechanisms

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for discussion.

## License
See LICENSE file for details.