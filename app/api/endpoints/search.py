from fastapi import APIRouter
from app.model.search_model import SearchQuery
from app.services.search_service import SearchService
from app.schema.search_schema import SearchResult

router = APIRouter(
    prefix="/search",
)

@router.post('/', summary="Hybrid Search Endpoint",
             description="The hybrid search endpoint allows users to perform searches combining traditional keyword-based methods and advanced semantic search techniques. By submitting a JSON payload, users can specify their query and choose the type of search they wish to perform.",
             )
def search(search_query: SearchQuery):
    try: 
        if search_query.search_type == 'keywords':
            return SearchService.keyword_seach(search_query)
        elif search_query.search_type == 'semantic':
            return SearchService.semantic_seach(search_query)
        elif search_query.search_type == 'hybrid':
            return SearchService.hybrid_search(search_query)
        else:
            return "Not found"
    except Exception as e:
        return {"status": "Error", "message": str(e)}