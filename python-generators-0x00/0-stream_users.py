import mysql.connector

# You'll need to use your own credentials and database name here
DB_NAME = "ALX_prodev"

def stream_users():
    """
    A generator that streams rows from the user_data table.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=USER,
            password= PASSWORD,
            database=DB_NAME
        )
        if not connection.is_connected():
            print(f"Error: Could not connect to the {DB_NAME} database.")
            return

        query = "SELECT * FROM user_data"
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            # The cursor object is an iterator. We loop over it once.
            for row in cursor:
                yield row
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    print("--- Starting data stream ---")
    row_count = 0
    
    # This loop consumes the generator one row at a time.
    for user_data in stream_users():
        print(f"Processing row: {user_data['name']}, Age: {user_data['age']}")
        row_count += 1
        
        if row_count >= 5:
            print("Stopped after processing 5 users to demonstrate efficiency.")
            break # The 'break' will cause the finally block to execute.
            
    print(f"\nTotal rows processed: {row_count}")