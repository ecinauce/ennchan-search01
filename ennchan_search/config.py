# src/config.py
import os
import json
import logging
from dataclasses import dataclass
from typing import Dict, Any, ClassVar, Optional

logger = logging.getLogger(__name__)

@dataclass
class Config:
    """
    Configuration class for the search module.
    
    This class holds all configuration parameters for the search module,
    including API keys, model settings, and RAG parameters.
    """
    # Environment variables
    BRAVE_API_KEY: str
    USER_AGENT: str
    
    def __post_init__(self):
        """Set environment variables after initialization."""
        os.environ["BRAVE_API_KEY"] = self.BRAVE_API_KEY
        os.environ["USER_AGENT"] = self.USER_AGENT

def load_config(config_path: str = None) -> Optional[Config]:
    """Load configuration from a JSON file."""
    if not config_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(script_dir), "config.json")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        
        config = Config(**config_data)
        print("Configuration loaded successfully")
        return config
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}.")
        return None