# ennchan_search_dev/ennchan_search/core/search.py
import logging
from typing import Optional, Dict, Union, List, Any

from ennchan_search.core.model import BraveSearchEngine

logger = logging.getLogger(__name__)

def search(query: str, config: Optional[Union[str, Dict]]=None) -> List[Dict[str, Any]]:
    """
    Search the web with improved error handling.
    
    Args:
        query: Search query
        config: Optional configuration
        
    Returns:
        List of search results with content
    """
    try:
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []
            
        logger.info(f"Initiating search for: {query}")
        engine = BraveSearchEngine(config)
        results = engine.search(query)
        
        logger.info(f"Search completed with {len(results)} results")
        return results
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []
