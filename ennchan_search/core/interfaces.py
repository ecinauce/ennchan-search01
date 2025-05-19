from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class SearchEngine(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def extract_content(self, url: str) -> Optional[str]:
        pass

    @abstractmethod
    def process_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class ResultExtractor(ABC):
    @abstractmethod
    def request_content(self) -> Optional[str]:
        pass

    @abstractmethod
    def process_result(self) -> List[Dict[str, Any]]:
        pass