import pytest
from ennchan_search.core.interfaces import SearchEngine, ResultExtractor

def test_search_engine_interface_cannot_be_instantiated():
    """Test that SearchEngine is an abstract class."""
    with pytest.raises(TypeError):
        SearchEngine()

def test_result_extractor_interface_cannot_be_instantiated():
    """Test that ResultExtractor is an abstract class."""
    with pytest.raises(TypeError):
        ResultExtractor()