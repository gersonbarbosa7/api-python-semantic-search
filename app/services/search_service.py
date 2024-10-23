from app.model.search_model import SearchQuery
from app.db.dbconnect import create_db_connection
from app.utils.embedding import convert_to_vector

class SearchService:
    def __init__(self):
        print("working")

    def hybrid_seach(search_query: SearchQuery):
        keywords = search_query.query.split()

        conn = create_db_connection()
        cursor = conn.cursor()

        # Keyword search SQL
        keyword_search_sql = f"""
            SELECT mi.id, 
                mi.title, 
                mi.author,
                mi.publication_date,
                mc.content
            FROM magazine_information mi
            JOIN magazine_content mc ON mi.id = mc.magazine_id
            WHERE mi.title ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                OR mi.author ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                OR mc.content ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}]);
        """

        cursor.execute(keyword_search_sql)
        keyword_results = cursor.fetchall()

        if keyword_results:  # Ensure there are results
            columns = [desc[0] for desc in cursor.description]  # Get the column names
            results = [dict(zip(columns, row)) for row in keyword_results]
        else:
            results = []

        cursor.close()
        conn.close()

        return {"results": results}
    
    def keyword_seach(search_query: SearchQuery):
        keywords = search_query.query.split()

        conn = create_db_connection()
        cursor = conn.cursor()

        # Keyword search SQL
        keyword_search_sql = f"""
            SELECT mi.id, 
                mi.title, 
                mi.author,
                mi.publication_date,
                mc.content
            FROM magazine_information mi
            JOIN magazine_content mc ON mi.id = mc.magazine_id
            WHERE mi.title ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                OR mi.author ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}])
                OR mc.content ILIKE ANY(ARRAY[{', '.join(["'%"+kw+"%'" for kw in keywords])}]);
        """

        cursor.execute(keyword_search_sql)
        keyword_results = cursor.fetchall()

        if keyword_results:  # Ensure there are results
            columns = [desc[0] for desc in cursor.description]  # Get the column names
            results = [dict(zip(columns, row)) for row in keyword_results]
        else:
            results = []

        cursor.close()
        conn.close()

        return {"results": results}
    
    def semantic_seach(search_query: SearchQuery):
        conn = create_db_connection()
        cursor = conn.cursor()

        # Vector search SQL
        # Assuming you have a function to convert query to vector
        query_vector = convert_to_vector(search_query.query)

        vector_search_sql = f"""
            SELECT mi.id, 
                mi.title, 
                mi.author,
                mi.publication_date,
                mc.content,
                mc.vector_representation <=> '{query_vector}' AS distance 
                FROM magazine_information mi JOIN magazine_content mc on mc.magazine_id = mi.id
                ORDER BY distance asc LIMIT 10
            """

        cursor.execute(vector_search_sql)
        vector_results = cursor.fetchall()

        if vector_results:  # Ensure there are results
            columns = [desc[0] for desc in cursor.description]  # Get the column names
            results = [dict(zip(columns, row)) for row in vector_results]
        else:
            results = []

        cursor.close()
        conn.close()

        return {"results": results}