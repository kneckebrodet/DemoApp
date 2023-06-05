import mysql.connector
from datetime import datetime, timedelta

class MySQL:
    def __init__(self):
        self.db = mysql.connector.connect(
            user='user',
            password='password',
            host='address',
            database='database'
        )

        self.cursor = self.db.cursor()

    def check_user_login(self, username):
        self.cursor.execute("SELECT * FROM user_table")
        all_users = self.cursor.fetchall()
        user_in_db = False
        userid = None
        for user_object in all_users:
            if username in user_object:
                user_in_db = True
                userid = user_object[0]
                break
        
        if user_in_db:
            return True, userid
        else:
            return False, None
        
    def check_if_entry_exists(self, id, table, date):
        query = "SELECT COUNT(*) FROM {} WHERE userID = %s AND date = %s".format(table)
        self.cursor.execute(query,(id,date))
        exists = self.cursor.fetchone()
        if exists[0]:
            return True
        else:
            return False

    def add_data(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())

        query = "INSERT INTO {} ({}) VALUES ({})".format(table, columns, placeholders)

        self.cursor.execute(query, values)
        self.db.commit()

    def get_wakeup_time(self, id):
        today = str(datetime.now().date())
        try:
            query = f"SELECT time FROM wutime_table WHERE userID = {id} AND date = '{today}'"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except:
            return None
        
    def get_bedtime(self,id):
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        try:
            query = f"SELECT time FROM wutime_table WHERE userID = {id} AND date = '{yesterday}'"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except:
            return None

    def update_data(self, id, table, data):
        today = str(datetime.now().date())
        # Construct the SET clause with the columns and new values
        set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
        set_clause = set_clause.replace("False", "0")
        set_clause = set_clause.replace("True", "1")

        query = f"UPDATE {table} SET {set_clause} WHERE userID = {id} AND date = '{today}'"
        
        self.cursor.execute(query)
        # Commit the changes to the database
        self.db.commit()

    def get_todo_list(self, id):
        query = f"SELECT task, detail FROM todo_table WHERE userID = {id}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        todo_list = {}
        for row in results:
            task, detail = row
            todo_list[task] = detail

        return todo_list
    
    def remove_task_from_db(self, id, task_name):
        try:
            query = f"DELETE FROM todo_table WHERE userID = {id} AND task = '{task_name}'"
            self.cursor.execute(query)
            self.db.commit()
            return 1
        except:
            return 0

    def get_stat(self, id, date, key):
        query = f"SELECT {key} FROM data_table WHERE userID = {id} AND date = '{date}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0]
    
    def check_if_available(self, username, password=""):
        self.cursor.execute("SELECT username FROM user_table")
        all_users = self.cursor.fetchall()
        username_is_available = False
        for user in all_users:
            if username in user:
                username_is_available = False
                break
            else:
                username_is_available = True

        if username == "": #or password == "":
            return False, "Please fill out all fields"
        elif not username_is_available:
            return False, f"\"{username}\" is already taken"
        else:

            return True, f"Successfully added \"{username}\" to database"

    def add_user(self, username, password=""):
        query = f"INSERT INTO user_table (username, password) VALUES (%s, NULL)"
        new_user = (username,)

        self.cursor.execute(query, new_user)
        self.db.commit()
