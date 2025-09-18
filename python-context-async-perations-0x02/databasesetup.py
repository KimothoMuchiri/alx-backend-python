import sqlite3
import csv
import uuid

TABLE_NAME = "user_data"
CSV_FILE = "python-generators-0x00/data.csv"

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        print("Successfully Connected!")
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

def insert_data(connection, csv_file):
    """Inserts data from a CSV file into the database."""
    query = f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (?, ?, ?, ?)"
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)  # Skip the header row
            for row in csvreader:
                user_id = str(uuid.uuid4())
                data_tuple = (user_id, row[0], row[1], float(row[2]))
                cursor.execute(query, data_tuple)
        connection.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")

def table_is_empty(connection) -> bool:
    query = f"SELECT COUNT(*) FROM {TABLE_NAME}"
    cursor = connection.cursor()
    cursor.execute(query)
    (count,) = cursor.fetchone()
    return count == 0

# Usage
with DatabaseConnection("ALX_pro_dev.db") as conn:
    cursor = conn.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY, 
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL
        )"""
    )
    
    if table_is_empty(conn):
        insert_data(conn, CSV_FILE)
    else:
        print("Table already has data.")
    conn.commit()

    # select and print all the users
    cursor.execute("SELECT * FROM user_data")
    results = cursor.fetchall()
    print("Results: ", results)