from pydantic import BaseModel

class SearchQuery(BaseModel):
    query: str
    search_type: str
    page: int = 0
    limit: int = 10