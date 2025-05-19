import os
import pytest
import tempfile
import json
from ennchan_search.config import Config, load_config

def test_config_initialization():
    """Test that Config initializes correctly with all parameters."""
    config = Config(
        BRAVE_API_KEY="test_key",
        USER_AGENT="test_agent",
        LANGSMITH_TRACING="true",
        LANGSMITH_API_KEY="test_langsmith",
        HUGGINGFACEHUB_API_TOKEN="test_hf",
        model_name="test_model",
        embeddings_model="test_embeddings",
        quantization=True,
        docs_source="test_docs",
        prompt_source="test_prompt",
        context_scope=2000
    )
    
    assert config.BRAVE_API_KEY == "test_key"
    assert config.model_name == "test_model"
    assert config.quantization is True
    assert os.environ.get("BRAVE_API_KEY") == "test_key"

def test_load_config():
    """Test loading config from a file."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        config_data = {
            "BRAVE_API_KEY": "test_key",
            "USER_AGENT": "test_agent",
            "LANGSMITH_TRACING": "true",
            "LANGSMITH_API_KEY": "test_langsmith",
            "HUGGINGFACEHUB_API_TOKEN": "test_hf",
            "model_name": "test_model"
        }
        json.dump(config_data, temp)
        temp_name = temp.name
    
    try:
        load_config(temp_name)
        # Verify environment variables were set
        assert os.environ.get("BRAVE_API_KEY") == "test_key"
    finally:
        os.unlink(temp_name)