import requests
from bs4 import BeautifulSoup

from ennchan_search.core.interfaces import ResultExtractor


class WebResultExtractor(ResultExtractor):
    def __init__(self, url: str):
        self.url = url
        self.result = ""
        self.ignore_tags = ['script', 'style', 'nav', 'header', 'footer']


    def request_content(self) -> str:
        try:
            # Basic request
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            
            self.result = response.text
            return self.process_result()
        
        except Exception as e:
            print(f"Error processing {self.url}: {e}")
            return ""
        

    def process_result(self) -> list:
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
        if not text:
            text = soup.body.get_text(separator='\n', strip=True)
        
        self.result = text
        return text
