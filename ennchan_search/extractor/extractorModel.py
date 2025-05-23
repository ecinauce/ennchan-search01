# ennchan_search_dev/ennchan_search/extractor/extractorModel.py
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

from ennchan_search.core.interfaces import ResultExtractor
from ennchan_search.utils.error_handling import retry_with_backoff

logger = logging.getLogger(__name__)

class WebResultExtractor(ResultExtractor):
    """
    Extracts content from web pages.
    
    This class handles fetching HTML content from URLs and extracting
    the main textual content while filtering out non-content elements.
    """
    
    def __init__(self, url: str):
        """
        Initialize the web content extractor.
        
        Args:
            url: The URL to extract content from
        """
        self.url = url
        self.result = ""
        self.ignore_tags = ['script', 'style', 'nav', 'header', 'footer']
        self.session = self._create_session()
    
    def _create_session(self):
        """Create a requests session with retry capabilities"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,  # Total number of retries
            backoff_factor=0.5,  # Backoff factor
            status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
            allowed_methods=["GET"]  # Only retry on GET requests
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @retry_with_backoff(max_retries=3, exceptions=(requests.RequestException,))
    def request_content(self) -> str:
        """
        Request and fetch content from the URL.
        
        Returns:
            Extracted text content from the URL or empty string if failed
            
        Raises:
            RequestException: If there's an issue with the HTTP request
        """
        try:
            logger.info(f"Requesting content from {self.url}")
            
            # Use session with retry capability
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = self.session.get(self.url, timeout=15, headers=headers)
            response.raise_for_status()
            
            self.result = response.text
            return self.process_result()
        
        except requests.RequestException as e:
            logger.error(f"Request error for {self.url}: {e}")
            raise  # Re-raise for retry decorator
        except Exception as e:
            logger.error(f"Unexpected error processing {self.url}: {e}")
            return ""

    def process_result(self) -> str:
        """
        Process the HTML content to extract meaningful text.
        
        This method removes non-content elements like scripts, styles,
        headers, and footers, then extracts text from paragraphs.
        
        Returns:
            Extracted text content or empty string if processing fails
        """
        try:
            # Parse HTML
            soup = BeautifulSoup(self.result, "html.parser")
            
            # Remove non-content elements
            for tag in self.ignore_tags:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Get paragraphs
            paragraphs = soup.find_all('p')
            text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30])
            
            # If no paragraphs found, get body text
            if not text and soup.body:
                text = soup.body.get_text(separator='\n', strip=True)
            
            # If still no text, try to get any text
            if not text:
                text = soup.get_text(separator='\n', strip=True)
            
            self.result = text
            return text
        except Exception as e:
            logger.error(f"Error parsing HTML from {self.url}: {e}")
            return ""