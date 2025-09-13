import mysql.connector
from mysql.connector import Error
from functools import wraps

# A simple in-memory cache
query_cache = {}

def cache_query(func):
    """
    A decorator that caches the results of a database query to
    avoid redundant calls.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Assuming the query is the second argument in the function call
        query = args[1]
        
        if query in query_cache:
            print(f"Cache hit! Returning cached results for: {query}")
            return query_cache[query]
        
        # If not in cache, call the original function to get the results
        print(f"Cache miss. Executing query and caching results for: {query}")
        result = func(*args, **kwargs)
        
        # Store the result in the cache before returning
        query_cache[query] = result
        
        return result
    return wrapper

def with_db_connection(func):
    """
    A decorator that handles opening and closing a database connection.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="ALX_prodev"
            )
            result = func(connection, *args, **kwargs)
            return result
        except Error as e:
            print(f"Error during database operation: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                connection.close()
    return wrapper

@with_db_connection
@cache_query
def execute_select_query(connection, query):
    """
    Executes a SELECT query and returns the results.
    """
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
    except Error as e:
        print(f"Error executing query: {e}")
        return None

if __name__ == '__main__':
    # Define a query to test caching
    query = "SELECT name, age FROM user_data WHERE age > 25 LIMIT 5"

    print("--- First call (should be a cache miss) ---")
    results1 = execute_select_query(query=query)
    print(f"Results from first call: {len(results1)} rows")
    print("-" * 30)
    
    # Run the same query again
    print("--- Second call (should be a cache hit) ---")
    results2 = execute_select_query(query=query)
    print(f"Results from second call: {len(results2)} rows")
    print("-" * 30)

    # Run a different query to test a new cache entry
    new_query = "SELECT name, email FROM user_data WHERE name LIKE 'A%' LIMIT 5"
    print("--- Third call with a different query (should be a new cache miss) ---")
    results3 = execute_select_query(query=new_query)
    print(f"Results from third call: {len(results3)} rows")