# ennchan_search_dev/ennchan_search/utils/error_handling.py
import time
import logging
from functools import wraps
from typing import Callable, TypeVar, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

T = TypeVar('T')

def retry_with_backoff(
    max_retries: int = 3, 
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_retries: Maximum number of retries
        initial_delay: Initial delay between retries in seconds
        backoff_factor: Factor by which the delay increases
        exceptions: Exceptions to catch and retry
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {e}"
                    )
                    
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            
            # If we get here, all retries failed
            raise last_exception or RuntimeError("All retries failed with unknown error")
        
        return wrapper
    
    return decorator

def safe_dict_get(d: dict, key_path: str, default: Any = None) -> Any:
    """
    Safely get a value from a nested dictionary using dot notation.
    
    Args:
        d: Dictionary to get value from
        key_path: Path to the key using dot notation (e.g., "web.results")
        default: Default value if key doesn't exist
        
    Returns:
        Value at the specified path or default
    """
    if not d:
        return default
        
    keys = key_path.split('.')
    result = d
    
    try:
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        return default
