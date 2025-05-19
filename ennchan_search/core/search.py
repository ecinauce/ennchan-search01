# -*- coding: utf-8 -*-
from ennchan_search.core.model import BraveSearchEngine
from typing import Optional, Dict, Union

def search(query: str, config: Optional[Union[str, Dict]]=None):
    engine = BraveSearchEngine(config)
    results = engine.search(query)
    return results