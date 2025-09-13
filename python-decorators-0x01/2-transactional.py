import mysql.connector
from mysql.connector import Error
from functools import wraps

def with_db_connection(func):
    """
    A decorator that handles opening and closing a database connection
    for the decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            # Open the database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="ALX_prodev"
            )
            print("Database connection opened.")
            
            # Pass the connection to the original function
            result = func(connection, *args, **kwargs)
            
            return result
        
        except Error as e:
            print(f"Error during database operation: {e}")
            return None
            
        finally:
            # Always close the connection
            if connection and connection.is_connected():
                connection.close()
                print("Database connection closed.")
    return wrapper

def transactional(func):
    """
    A decorator that ensures a function running a database operation
    is wrapped inside a transaction.
    """
    @wraps(func)
    def wrapper(connection, *args, **kwargs):
        try:
            # Call the decorated function with the connection
            result = func(connection, *args, **kwargs)
            # If no errors, commit the transaction
            connection.commit()
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            # If any error occurs, roll back the transaction
            if connection:
                connection.rollback()
                print(f"Transaction rolled back due to an error: {e}")
            raise # Re-raise the exception to be handled by the outer decorator
    return wrapper

# You can stack the decorators here. The order matters!
# The inner decorator (@transactional) will be executed first.
@with_db_connection
@transactional
def insert_multiple_users(connection, users):
    """
    Inserts a list of users into the database.
    Will commit all or none.
    """
    query = "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)"
    try:
        with connection.cursor() as cursor:
            for user in users:
                cursor.execute(query, (user['name'], user['email'], user['age']))
            return cursor.rowcount
    except Error as e:
        print(f"Inner function error: {e}")
        raise # Re-raise the error to trigger the rollback
        
if __name__ == '__main__':
    # Example 1: Successful transaction
    print("--- Attempting to insert two users ---")
    new_users = [
        {"name": "Alice", "email": "alice@example.com", "age": 28},
        {"name": "Bob", "email": "bob@example.com", "age": 35}
    ]
    rows_inserted = insert_multiple_users(users=new_users)
    print(f"Number of rows inserted: {rows_inserted}")

    print("\n" + "="*40 + "\n")

    # Example 2: Failed transaction (due to duplicate email)
    print("--- Attempting to insert a user with a duplicate email ---")
    # This will fail and trigger a rollback
    failing_users = [
        {"name": "Charlie", "email": "charlie@example.com", "age": 42},
        {"name": "Alice", "email": "alice@example.com", "age": 28} # Duplicate email
    ]
    try:
        insert_multiple_users(users=failing_users)
    except Exception as e:
        print(f"Caught the re-raised exception: {e}")