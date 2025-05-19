import pytest
from unittest.mock import patch, MagicMock
from ennchan_search.extractor.extractorModel import WebResultExtractor

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.text = "<html><body><p>Test paragraph 1</p><p>Test paragraph 2</p></body></html>"
    mock.raise_for_status = MagicMock()
    return mock

@patch('ennchan_search.extractor.extractorModel.requests.get')
def test_request_content(mock_get, mock_response):
    """Test requesting content from a URL."""
    mock_get.return_value = mock_response
    
    extractor = WebResultExtractor("https://example.com")
    result = extractor.request_content()
    
    assert "Test paragraph 1" in result
    assert "Test paragraph 2" in result

def test_process_result():
    """Test processing HTML content."""
    extractor = WebResultExtractor("https://example.com")
    extractor.result = """
    <html>
        <head><script>var x = 1;</script><style>.test{color:red;}</style></head>
        <body>
            <header>Header content</header>
            <p>Important paragraph 1</p>
            <p>Important paragraph 2</p>
            <footer>Footer content</footer>
        </body>
    </html>
    """
    
    result = extractor.process_result()
    
    assert "Important paragraph 1" in result
    assert "Important paragraph 2" in result
    assert "Header content" not in result
    assert "Footer content" not in result