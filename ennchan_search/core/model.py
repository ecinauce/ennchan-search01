# ennchan_search_dev/ennchan_search/core/model.py
from brave import Brave
from typing import Optional, List, Dict, Any, Union
import json
import os
import time
import logging
import concurrent.futures
from requests.exceptions import RequestException

from ennchan_search.core.interfaces import SearchEngine
from ennchan_search.extractor.extractorModel import WebResultExtractor
from ennchan_search.config import Config, load_config
from ennchan_search.utils.error_handling import retry_with_backoff, safe_dict_get

logger = logging.getLogger(__name__)

class BraveSearchEngine(SearchEngine):
    """
    Search engine implementation using Brave Search API.
    
    This class provides search functionality using the Brave Search API
    and handles content extraction from search results.
    """
    
    def __init__(self, config: Optional[Union[str, Dict, Config]] = None):
        """
        Initialize the Brave Search engine.
        
        Args:
            config: Configuration for the search engine. Can be a path to a config file,
                   a dictionary, a Config object, or None to use environment variables.
        """
        # Handle different config types
        if isinstance(config, str):
            # If config is a string path, load it
            try:
                with open(config, 'r') as f:
                    config_data = json.load(f)
                self.api_key = config_data.get("BRAVE_API_KEY")
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
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
            logger.info("Initialized Brave Search with API key")
        else:
            self.brave = Brave()
            logger.warning("Initialized Brave Search without API key")

    def extract_content(self, url: str) -> Optional[str]:
        """
        Extract main content from a URL with improved error handling.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            Extracted content as string or None if extraction fails
        """
        try:
            logger.info(f"Extracting content from {url}")
            output = WebResultExtractor(url)
            content = output.request_content()
            
            if not content:
                logger.warning(f"No content extracted from {url}")
            
            return content
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {e}")
            return None

    def process_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process search results with improved error handling.
        
        This method extracts relevant information from search results,
        fetches content from each URL, and returns processed results.
        
        Args:
            results: Raw search results from the Brave API
            
        Returns:
            List of processed search results with extracted content
        """
        try:
            # Safely get results using helper function
            web_results = safe_dict_get(results, 'web.results', [])
            
            if not web_results:
                logger.warning("No web results found in search response")
                return []
            
            # Extract important fields with defensive programming
            pre_proc = []
            for result in web_results:
                if not isinstance(result, dict):
                    continue
                    
                item = {
                    "title": result.get("title", "Untitled"),
                    "url": result.get("url", ""),
                    "description": result.get("description", "")
                }
                
                # Skip items without URL
                if not item["url"]:
                    logger.warning("Skipping result with no URL")
                    continue
                    
                pre_proc.append(item)
            
            logger.info(f"Processing {len(pre_proc)} search results")
            
            # Extract content from each URL in parallel
            output = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Submit all tasks
                future_to_url = {
                    executor.submit(self._process_single_url, result): result 
                    for result in pre_proc
                }
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(future_to_url):
                    result = future_to_url[future]
                    try:
                        processed_result = future.result()
                        if processed_result:
                            output.append(processed_result)
                    except Exception as e:
                        url = result.get("url", "unknown URL")
                        logger.error(f"Error processing {url}: {e}")
            
            logger.info(f"Successfully processed {len(output)} out of {len(pre_proc)} results")
            return output
            
        except Exception as e:
            logger.error(f"Error processing search results: {e}")
            return []

    def _process_single_url(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single URL with error handling.
        
        This method extracts content from a single URL and formats it
        into a structured result.
        
        Args:
            result: Search result item containing URL and metadata
            
        Returns:
            Processed result with extracted content or None if processing fails
        """
        url = result.get("url")
        if not url:
            logger.warning("Result missing URL")
            return None
            
        try:
            logger.info(f"Processing {url}")
            content = self.extract_content(url)
            
            # Return result if content was extracted
            if content:
                return {
                    "title": result.get("title", "Unknown Title"),
                    "url": url,
                    "description": result.get("description", ""),
                    "content": content
                }
            else:
                logger.warning(f"No content extracted from {url}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            return None

    @retry_with_backoff(max_retries=5, initial_delay=1.0, backoff_factor=2.0)
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search with improved error handling and retries.
        
        This method performs a search using the Brave API with
        automatic retries and comprehensive error handling.
        
        Args:
            query: The search query string
            
        Returns:
            List of search results with extracted content
            
        Raises:
            Exception: If all retry attempts fail
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []
            
        try:
            logger.info(f"Searching for: {query}")
            search_results = self.brave.search(q=query, raw=True)
            
            # Validate search results
            if not search_results:
                logger.warning("Empty search results returned")
                return []
                
            if not isinstance(search_results, dict):
                logger.warning(f"Unexpected search results type: {type(search_results)}")
                return []
                
            if "web" not in search_results or "results" not in search_results.get("web", {}):
                logger.warning("Invalid search results format")
                return []
                
            # Process results
            return self.process_results(search_results)
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            raise  # Re-raise for retry decorator