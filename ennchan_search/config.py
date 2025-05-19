# src/config.py
import os
import json
from dataclasses import dataclass
from typing import Dict, Any, ClassVar

@dataclass
class Config:
    # Environment variables
    BRAVE_API_KEY: str
    USER_AGENT: str
    LANGSMITH_TRACING: str
    LANGSMITH_API_KEY: str
    HUGGINGFACEHUB_API_TOKEN: str
    
    # Model settings
    model_name: str
    embeddings_model: str
    quantization: bool
    
    # RAG settings
    docs_source: str
    prompt_source: str
    context_scope: int
    
    # Default values as class variables
    DEFAULTS: ClassVar[Dict[str, Any]] = {
        "model_name": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "embeddings_model": "sentence-transformers/all-MiniLM-L6-v2",
        "quantization": False,
        "docs_source": "https://en.wikipedia.org/wiki/World_War_II",
        "prompt_source": "rlm/rag-prompt",
        "context_scope": 1000
    }
    
    def __post_init__(self):
        # Set environment variables
        os.environ["BRAVE_API_KEY"] = self.BRAVE_API_KEY
        os.environ["USER_AGENT"] = self.USER_AGENT
        os.environ["LANGSMITH_TRACING"] = self.LANGSMITH_TRACING
        os.environ["LANGSMITH_API_KEY"] = self.LANGSMITH_API_KEY
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = self.HUGGINGFACEHUB_API_TOKEN

# Load configuration

def load_config(config_path: str = None) -> None:
    if not config_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(script_dir), "config.json")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        
        # Apply defaults for missing values
        for key, default in Config.DEFAULTS.items():
            if key not in config_data:
                config_data[key] = default
        
        Config(**config_data)
        print("Configuration loaded successfully")
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}.")
        exit(1)
