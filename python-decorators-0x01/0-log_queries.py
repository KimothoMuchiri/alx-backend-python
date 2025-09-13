import mysql.connector
from mysql.connector import Error

def log_queries(func):
    """
    A decorator that logs the SQL query before it is executed.
    """
    ["from datetime import datetime"]
    def wrapper(*args, **kwargs):
        # The 'args' tuple will contain the database connection and the query
        if len(args) > 1:
            query = args[1]
            print(f"Executing query: {query}")
        else:
            print("No SQL query found to log.")
        return func(*args, **kwargs)
    return wrapper

def connect_to_prodev():
    # Use your own credentials here
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

@log_queries
def execute_query(connection, query):
    """
    A function that executes a given SQL query.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            # Fetch results if it's a SELECT query
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                print(f"Query returned {len(results)} rows.")
            else:
                connection.commit()
                print("Query executed successfully.")
    except Error as e:
        print(f"Error executing query: {e}")

if __name__ == '__main__':
    # Connect to the database
    conn = connect_to_prodev()
    if conn:
        # Example usage of the decorated function
        execute_query(conn, "SELECT name, age FROM user_data LIMIT 5")
        execute_query(conn, "CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)")
        conn.close()