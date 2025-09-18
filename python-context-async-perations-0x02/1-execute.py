import sqlite3
class ExecuteQuery:
    def __init__(self, db_name, query,params= None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.results = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        print("Query results:", self.results)
        return self.results

    def __exit__(self, exc_type,exc_value,traceback):
        if self.connection:
            self.connection.close()



with ExecuteQuery("ALX_pro_dev", "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print("Users older than 25: ", results)
    



        