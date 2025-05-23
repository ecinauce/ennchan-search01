# Ennchan Search Engine Module

A modular search engine component designed for RAG (Retrieval-Augmented Generation) systems.

## Project Overview

### What is this?
This is a search engine module that handles web searching and content extraction. It's designed to be a component in RAG systems, providing efficient web content retrieval and processing capabilities.

### Why build it?
This module serves as a crucial component for RAG systems, handling the retrieval aspect by providing:
- Flexible search engine integration
- Robust content extraction
- Efficient processing of web results
- Clean integration interfaces for larger systems

## Features

### Core Functionality
- Configurable search engine integration (currently supports Brave Search)
- Advanced content extraction from web pages
- Parallel processing of search results
- Error handling with retry mechanisms

### Technical Architecture

#### Search and Retrieval Pipeline
1. Query Processing
   - Clean query handling
   - Search optimization

2. Search Integration
   - Brave Search API integration
   - Robust error handling and retry mechanisms
   - Asynchronous request handling

3. Content Extraction
   - HTML content processing
   - Main content identification
   - Noise filtering (ads, navigation, etc.)
   - Text cleaning and formatting

## Optimizations

### Performance Enhancements
- Multiprocessing for parallel content extraction
- Network request batching and retry mechanisms
- Efficient HTML processing
- Request caching capabilities

### Resource Management
- Configurable batch sizes for processing
- Memory-efficient data structures
- Stream processing for large results

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
query = "your search query"
results = search(query, config)
```

### Advanced Usage
```python
from ennchan_search.core.model import BraveSearchEngine

# Initialize with custom configuration
engine = BraveSearchEngine(config)

# Perform search
results = engine.search("your query")

# Extract content from a specific URL
content = engine.extract_content("https://example.com")
```

## Interfaces

### Core Components
- SearchEngine: Base interface for search implementations
- ResultExtractor: Interface for content extraction
- BraveSearchEngine: Implementation of Brave search
- WebResultExtractor: Web content extraction implementation

## Future Development
- Additional search engine integrations
- Enhanced content extraction strategies
- Improved caching mechanisms
- Additional result filtering options

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for discussion.

## License
See LICENSE file for details.