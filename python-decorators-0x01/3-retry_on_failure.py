import mysql.connector
from mysql.connector import Error
from functools import wraps
import time

def retry_on_failure(retries=3, delay=2):
    """
    A decorator that retries a function a specified number of times
    if it raises an exception.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {i + 1}/{retries} failed: {e}")
                    if i < retries - 1:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed. Raising the exception.")
                        raise
        return wrapper
    return decorator

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

@retry_on_failure(retries=5, delay=3)
@with_db_connection
def get_user_by_id(connection, user_id):
    """
    Fetches a user by their ID.
    This function will be retried on failure.
    """
    if user_id == "failing_id":
        raise Error("Simulated transient connection error.")
        
    query = "SELECT * FROM user_data WHERE user_id = %s"
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            print("Successfully fetched user.")
            return user
    except Error as e:
        print(f"Error executing query: {e}")
        return None

if __name__ == '__main__':
    # Example 1: Successful operation
    print("--- Attempting to fetch a valid user ID ---")
    valid_id = "some_valid_user_id" # Replace with a valid UUID from your database
    user_data = get_user_by_id(user_id=valid_id)
    print(f"User data: {user_data}")
    print("\n" + "="*40 + "\n")

    # Example 2: Simulated failure with retries
    print("--- Attempting to fetch a failing user ID ---")
    failing_id = "failing_id"
    user_data = get_user_by_id(user_id=failing_id)
    print("Operation finished.")