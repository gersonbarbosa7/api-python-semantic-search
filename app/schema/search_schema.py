from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BaseSearch(BaseModel):
    id: int
    title: str
    author: str
    publication_date: datetime
    content: str

class SearchResult(BaseModel):
    results: Optional[List[BaseSearch]]