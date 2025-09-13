import mysql.connector

# Use your credentials and database name here
DB_NAME = "ALX_prodev"

def stream_user_ages():
    """
    A generator that fetches and yields user ages one by one.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        if not connection or not connection.is_connected():
            print(f"Error: Could not connect to the {DB_NAME} database.")
            return

        query = "SELECT age FROM user_data"
        with connection.cursor() as cursor:
            cursor.execute(query)
            
            # This is the first loop
            for (age,) in cursor: # The comma unpacks the tuple returned by the cursor
                yield age
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")

def calculate_average_age():
    """
    Calculates the average age using a generator to avoid
    loading the entire dataset into memory.
    """
    total_age = 0
    user_count = 0
    
    # This is the second loop
    for age in stream_user_ages():
        total_age += age
        user_count += 1
        
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No user data found to calculate the average age.")

# Call the main function to run the script
if __name__ == "__main__":
    calculate_average_age()