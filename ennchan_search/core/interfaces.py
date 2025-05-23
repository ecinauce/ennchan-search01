from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class SearchEngine(ABC):
    """
    Abstract base class for search engine implementations.
    
    This interface defines the required methods for any search engine
    implementation in the system.
    """
    
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for information based on the query.
        
        Args:
            query: The search query string
            
        Returns:
            List of search results as dictionaries
        """
        pass

    @abstractmethod
    def extract_content(self, url: str) -> Optional[str]:
        """
        Extract content from a URL.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            Extracted content as string or None if extraction fails
        """
        pass

    @abstractmethod
    def process_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process search results to extract and format content.
        
        Args:
            results: Raw search results to process
            
        Returns:
            Processed search results with extracted content
        """
        pass


class ResultExtractor(ABC):
    """
    Abstract base class for content extraction implementations.
    
    This interface defines the required methods for any content extractor
    implementation in the system.
    """
    
    @abstractmethod
    def request_content(self) -> Optional[str]:
        """
        Request content from a source.
        
        Returns:
            Extracted content as string or None if extraction fails
        """
        pass

    @abstractmethod
    def process_result(self) -> List[Dict[str, Any]]:
        """
        Process the raw content into structured format.
        
        Returns:
            Processed content in structured format
        """
        pass