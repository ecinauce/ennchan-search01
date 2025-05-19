import pytest
from unittest.mock import patch
from ennchan_search.core.search import search

@patch('ennchan_search.core.model.BraveSearchEngine.search')
def test_search_function(mock_search):
    """Test the main search function."""
    mock_search.return_value = [{"title": "Test", "url": "https://example.com"}]
    
    results = search("test query")
    
    assert len(results) == 1
    assert results[0]["title"] == "Test"
    mock_search.assert_called_once_with("test query")