import pytest
import os

@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables."""
    os.environ["BRAVE_API_KEY"] = "test_key"
    os.environ["USER_AGENT"] = "test_agent"
    os.environ["LANGSMITH_TRACING"] = "false"
    os.environ["LANGSMITH_API_KEY"] = "test_key"
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "test_token"
    yield
    # Clean up after tests
    for key in ["BRAVE_API_KEY", "USER_AGENT", "LANGSMITH_TRACING", 
                "LANGSMITH_API_KEY", "HUGGINGFACEHUB_API_TOKEN"]:
        if key in os.environ:
            del os.environ[key]