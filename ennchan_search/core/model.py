from brave import Brave
from typing import Optional, List, Dict, Any, Union

from ennchan_search.core.interfaces import SearchEngine
from ennchan_search.extractor.extractorModel import WebResultExtractor

import json
import os
from ennchan_search.config import Config, load_config

class BraveSearchEngine(SearchEngine):
    def __init__(self, config: Optional[Union[str, Dict, Config]] = None):
        # Handle different config types
        if isinstance(config, str):
            # If config is a string path, load it
            try:
                with open(config, 'r') as f:
                    config_data = json.load(f)
                self.api_key = config_data.get("BRAVE_API_KEY")
            except Exception as e:
                print(f"Error loading config file: {e}")
                self.api_key = None
        elif isinstance(config, dict):
            # If config is a dictionary
            self.api_key = config.get("BRAVE_API_KEY")
        elif hasattr(config, 'BRAVE_API_KEY'):
            # If config is a Config object
            self.api_key = config.BRAVE_API_KEY
        else:
            # Default case
            self.api_key = os.environ.get("BRAVE_API_KEY")
        
        # Initialize Brave API
        if self.api_key:
            self.brave = Brave(api_key=self.api_key)
        else:
            self.brave = Brave()



    def extract_content(self, url: str) -> Optional[str]:    
        """Extract main content from a URL - simplified version"""
        output = WebResultExtractor(url)
        output.request_content()
        return output.result


    def process_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Get only important fields
        pre_proc = results["web"]["results"]
        pre_proc = [{
            "title": result["title"],
            "url": result["url"],
            "description": result["description"],
        } for result in pre_proc]

        # Extract content from each URL
        output = []
        # Can be threaded for performance
        for result in pre_proc:
            print(f"Processing {result['url']}")
            url = result["url"]
            content = self.extract_content(url)
            
            # Collate contents if exist
            if content:
                output.append({
                    "title": result["title"],
                    "url": url,
                    "description": result["description"],
                    "content": content
                })
        
        return output


    def search(self, query: str) -> List[Dict[str, Any]]:
        retry = 5
        while retry > 0:
            try:
                search_results = self.brave.search(q=query, raw=True)
                break
            except Exception as e:
                print(f"Error: {e}")
                retry -= 1
                if retry == 0:
                    raise e

        output = self.process_results(search_results)
        return output