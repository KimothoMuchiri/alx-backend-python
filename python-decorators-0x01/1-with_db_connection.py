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
            
            # Commit changes for write operations
            if connection.is_connected():
                connection.commit()
            
            return result
        
        except Error as e:
            print(f"Error during database operation: {e}")
            if connection and connection.is_connected():
                connection.rollback() # Rollback on error
            return None
            
        finally:
            # Always close the connection
            if connection and connection.is_connected():
                connection.close()
                print("Database connection closed.")
    return wrapper

@with_db_connection
def get_user_by_email(connection, email):
    """
    Fetches a user from the database based on their email.
    """
    query = "SELECT * FROM user_data WHERE email = %s"
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user
    except Error as e:
        print(f"Error executing query: {e}")
        return None

@with_db_connection
def insert_new_user(connection, name, email, age):
    """
    Inserts a new user into the database.
    """
    query = "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (name, email, age))
            print("New user inserted successfully!")
            return cursor.rowcount
    except Error as e:
        print(f"Error inserting user: {e}")
        return 0

if __name__ == '__main__':
    # --- Example 1: Fetching data ---
    print("--- Getting user by email ---")
    user_email = "janedoe@example.com"
    user_data = get_user_by_email(email=user_email)
    if user_data:
        print(f"User found: {user_data['name']}")
    else:
        print("User not found.")

    # --- Example 2: Inserting data ---
    print("\n--- Inserting new user ---")
    rows_affected = insert_new_user(name="John Doe", email="johndoe@example.com", age=30)
    print(f"Rows affected: {rows_affected}")

    # The decorator handles the connection and closure for each function call