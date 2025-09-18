import sqlite3

# Class definition
class  DatabaseConnection:
    def __init__(self,db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        print("Successfully Connected!")
        return self.connection

    def __exit__(self,exc_type,exc_value,traceback):
        if self.connection:
            self.connection.close()

# Class usage

with DatabaseConnection("ALX_pro_dev") as conn:
    # get a cursor object to execute the queries
    cursor = conn.cursor()
    
    # optional - create the table and insert some values if it doesn't exist
    # cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    # Insert some data
    # cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (1, 'Alice'))
    # cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (2, 'Bob'))
    # print(f"User {user_id} ({name}) inserted.")
    # conn.commit()

    # select and print all the users
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Results: ", results)
   
    
