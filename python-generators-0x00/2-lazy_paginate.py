import mysql.connector

# Use your credentials and database name here
DB_NAME = "ALX_prodev"

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        if not connection.is_connected():
            print(f"Error: Could not connect to the {DB_NAME} database.")
            return []

        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()  # This returns a list of dictionaries (the page)
            
    except mysql.connector.Error as e:
        print(f"Error fetching page: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

def lazy_paginate(page_size):
    """
    A generator that lazily fetches and yields pages of user data.
    """
    offset = 0
    while True: # This is the single loop
        page = paginate_users(page_size, offset)
        
        if not page:
            break # No more pages to fetch, exit the loop
            
        yield page
        
        offset += page_size