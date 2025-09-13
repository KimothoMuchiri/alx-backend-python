import mysql.connector

# Use your credentials and database name here
DB_NAME = "ALX_prodev"

def stream_users_in_batches(batch_size):
    """
    A generator that fetches rows in batches from the user_data table.
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
            return

        query = "SELECT * FROM user_data"
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            
            while True:
                # Fetch a batch of rows
                rows = cursor.fetchmany(batch_size)
                
                if not rows:
                    break  # No more rows to fetch
                
                yield rows
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")

def batch_processing(batch_size):
    """
    Processes each batch of users to filter those over the age of 25.
    """
    processed_count = 0
    
    # This is the second loop, iterating over the batches from the generator
    for batch in stream_users_in_batches(batch_size):
        # This is the third loop, iterating over the rows within each batch
        for user in batch:
            if user['age'] > 25:
                print(f"User {user['name']} is over 25.")
                processed_count += 1
                
    print(f"\nCompleted processing. Found {processed_count} users over 25.")