import pytest
from unittest.mock import patch, MagicMock
from ennchan_search.core.model import BraveSearchEngine

@pytest.fixture
def mock_config():
    return MagicMock(BRAVE_API_KEY="test_key")

@pytest.fixture
def mock_brave_response():
    return {
        "web": {
            "results": [
                {
                    "title": "Test Title",
                    "url": "https://example.com",
                    "description": "Test Description"
                }
            ]
        }
    }

@patch('ennchan_search.core.model.Brave')
def test_brave_search_engine_initialization(mock_brave, mock_config):
    """Test BraveSearchEngine initialization."""
    engine = BraveSearchEngine(mock_config)
    mock_brave.assert_called_once_with(api_key="test_key")

@patch('ennchan_search.core.model.WebResultExtractor')
@patch('ennchan_search.core.model.Brave')
def test_search_method(mock_brave, mock_extractor, mock_config, mock_brave_response):
    """Test search method returns processed results."""
    # Setup mocks
    mock_brave_instance = MagicMock()
    mock_brave_instance.search.return_value = mock_brave_response
    mock_brave.return_value = mock_brave_instance
    
    mock_extractor_instance = MagicMock()
    mock_extractor_instance.result = "Test Content"
    mock_extractor.return_value = mock_extractor_instance
    
    # Execute
    engine = BraveSearchEngine(mock_config)
    results = engine.search("test query")
    
    # Assert
    assert len(results) == 1
    assert results[0]["title"] == "Test Title"
    assert results[0]["url"] == "https://example.com"
    assert "content" in results[0]