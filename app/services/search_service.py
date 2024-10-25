from app.model.search_model import SearchQuery
from app.db.dbconnect import create_db_connection
from app.utils.embedding import convert_to_vector
from app.utils.support_date import convert_dates_to_string
import json
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class SearchService:
    def __init__(self):
        print("working")

    def hybrid_search(search_query: SearchQuery):
        keywords = search_query.query.split()

        # Create a cache key
        cache_key = f"search:{search_query.query}:{search_query.search_type}:{search_query.page}:{search_query.limit}"
        cached_result = redis_client.get(cache_key)

        if cached_result:
            return json.loads(cached_result)  # Return cached result
        
        offset = search_query.page * search_query.limit
        limit = search_query.limit

        # Semantic search
        query_vector = convert_to_vector(search_query.query)
        
        conn = create_db_connection()
        cursor = conn.cursor()

        # Keyword search SQL
        sql_keywords = f"""
            WITH CTE AS (
                SELECT mi.id, 
                    mi.title, 
                    mi.author,
                    mi.publication_date,
                    mc.content,
                    mc.vector_representation <=> '{query_vector}' AS distance 
                    FROM magazine_information mi
                    JOIN magazine_content mc ON mi.id = mc.magazine_id
                    WHERE mi.title ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                    OR mi.author ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                    OR mc.content ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
            )
            SELECT (SELECT COUNT(*) AS total_rows FROM CTE), *
                FROM CTE 
                ORDER BY distance ASC, id DESC
                LIMIT {limit} 
                OFFSET {offset}; 
        """

        cursor.execute(sql_keywords)
        keyword_results = cursor.fetchall()

        total_rows = 0

        if keyword_results:  # Ensure there are results
            columns = [desc[0] for desc in cursor.description]  # Get the column names
            results = [dict(zip(columns, row)) for row in keyword_results]
            total_rows = results[0]['total_rows']
        else:
            results = []

        cursor.close()
        conn.close()

        # Combine both keyword and vector results
        # combined_results = keyword_data + vector_data
        combined_results = convert_dates_to_string(results)

        result_query = {"results": combined_results, "total_rows": total_rows, "limit": limit}

        redis_client.set(cache_key, json.dumps(result_query), ex=3600)  # Cache for 1 hour

        # Return as a single result list
        return result_query
    
    def keyword_seach(search_query: SearchQuery):
        keywords = search_query.query.split()

        # Create a cache key
        cache_key = f"search:{search_query.query}:{search_query.search_type}:{search_query.page}:{search_query.limit}"
        cached_result = redis_client.get(cache_key)

        if cached_result:
            return json.loads(cached_result)  # Return cached result
        
        offset = search_query.page * search_query.limit
        limit = search_query.limit
        
        conn = create_db_connection()
        cursor = conn.cursor()

        # Keyword search SQL
        sql_query = f"""
            WITH CTE AS (
                SELECT mi.id, 
                    mi.title, 
                    mi.author,
                    mi.publication_date,
                    mc.content
                    FROM magazine_information mi
                    JOIN magazine_content mc ON mi.id = mc.magazine_id
                    WHERE mi.title ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                    OR mi.author ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                    OR mc.content ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
            )
            SELECT (SELECT COUNT(*) AS total_rows FROM CTE), *
                FROM CTE 
                ORDER BY id DESC 
                LIMIT {limit} 
                OFFSET {offset};
        """

        cursor.execute(sql_query)
        keyword_results = cursor.fetchall()
        total_rows = 0

        if keyword_results:  # Ensure there are results
            columns = [desc[0] for desc in cursor.description]  # Get the column names
            results = [dict(zip(columns, row)) for row in keyword_results]
            total_rows = results[0]['total_rows']
        else:
            results = []

        cursor.close()
        conn.close()

        results = convert_dates_to_string(results)

        result_query = {
            "results": results, 
            "total_rows": total_rows, 
            "limit": limit
        }

        redis_client.set(cache_key, json.dumps(result_query), ex=3600)  # Cache for 1 hour

        return result_query
    
    def semantic_seach(search_query: SearchQuery):

        # Create a cache key
        cache_key = f"search:{search_query.query}:{search_query.search_type}:{search_query.page}:{search_query.limit}"
        cached_result = redis_client.get(cache_key)

        if cached_result:
            return json.loads(cached_result)  # Return cached result

        offset = search_query.page * search_query.limit
        limit = search_query.limit
        
        conn = create_db_connection()
        cursor = conn.cursor()

        # Vector search SQL
        # Assuming you have a function to convert query to vector
        query_vector = convert_to_vector(search_query.query)

        sql_vector_search = f"""
            WITH CTE AS (
                SELECT mi.id, 
                    mi.title, 
                    mi.author,
                    mi.publication_date,
                    mc.content,
                    mc.vector_representation <=> '{query_vector}' AS distance 
                    FROM magazine_information mi 
                    JOIN magazine_content mc on mc.magazine_id = mi.id
            )
            SELECT (SELECT COUNT(*) AS total_rows FROM CTE), *
                FROM CTE 
                ORDER BY distance ASC, id DESC 
                LIMIT {limit} 
                OFFSET {offset};
            """
        
        cursor.execute(sql_vector_search)
        vector_results = cursor.fetchall()
        total_rows = 0

        if vector_results:  # Ensure there are results
            columns = [desc[0] for desc in cursor.description]  # Get the column names
            results = [dict(zip(columns, row)) for row in vector_results]
            total_rows = results[0]['total_rows']
        else:
            results = []

        cursor.close()
        conn.close()

        results = convert_dates_to_string(results)

        result_query = {"results": results, "total_rows": total_rows, "limit": limit}

        redis_client.set(cache_key, json.dumps(result_query), ex=3600)  # Cache for 1 hour

        return result_query