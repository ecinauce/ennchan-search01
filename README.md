# Ennchan Search Engine Module 01
Multi Search Engine Module for use with a RAG project.

## Installation:

`pip install ennchan-search-*.whl`

(*Best do it inside a venv*)


## How to use:
### Config
Filename: config.json
```json
{
    "BRAVE_API_KEY": "please get your own key"
}
```
### Code
```python
from ennchan_search import search

config = "path/to/config.json"
query = "Ennchan"
answers = ask(query, config)
```
