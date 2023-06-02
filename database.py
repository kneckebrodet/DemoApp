#from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
from pymongo import MongoClient
from datetime import datetime, timedelta

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect_to_localhost(self, address="127.0.0.1", port = 27017):
        #uri = "mongodb+srv://kneckebrodet:yJrVvEyUDONN@myappdb.j1cqx44.mongodb.net/?retryWrites=true&w=majority"
        #self.client = MongoClient(uri)
        self.client = MongoClient(address, port)

        self.db = self.client.myappDB
        # Choose collection
        self.user_collection = self.db.user_collection
        self.data_collection = self.db.data_collection
        self.todo_collection = self.db.todo_collection
        self.bedtime_collection = self.db.bedtime_collection
        self.wutime_collection = self.db.wutime_collection

    def add_user(self, id, username):
        user_data = {"userID":id, "username":username}
        self.user_collection.insert_one(user_data)

    def add_data(self, collection, data):
        if collection == "data_collection":
            self.data_collection.insert_one(data)
        elif collection == "todo_collection":
            self.todo_collection.insert_one(data)
        elif collection == "bedtime_collection":
            self.bedtime_collection.insert_one(data)
        elif collection == "wutime_collection":
            self.wutime_collection.insert_one(data)

    def get_bedtime(self, id):
        # find yesterday bedtime
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        try:
            time = self.bedtime_collection.find_one({"userID": id, "date":yesterday})["time"]
            return time
        except:
            return None

    def get_wakeup_time(self, id):
        today = str(datetime.now().date())
        try:
            time = self.wutime_collection.find_one({"userID": id, "date":today})["time"]
            return time
        except:
            return None

    def get_todo_list(self, id):
        todolist = self.todo_collection.find({"userID":id}, {"_id": 0})
        new_list = {}
        for item in todolist:
            new_list[item["task"]] = item["detail"]
        return new_list

    def get_user_list(self):
        user_objects = self.user_collection.find({},{"_id": 0})
        user_list = []
        for obj in user_objects:
            user_list.append(obj["username"])
        return user_list

    def get_id_list(self):
        user_objects = self.user_collection.find({},{"_id": 0})
        id_list = []
        for obj in user_objects:
            id_list.append(obj["userID"])
        return id_list

    def get_id(self, username):
        userobject = self.user_collection.find_one({"username":username})
        return userobject["userID"]

    def check_if_available(self, id, username):
        userlist = self.get_user_list()
        idlist = self.get_id_list()

        if id == "" or username == "":
            return False, "Please fill out all fields"
        elif not id.isdigit():
            return False, "User ID must be only digits"
        elif id in idlist and username in userlist:
            return False, "ID and Username already exist"
        elif id in idlist:
            return False, "ID already taken"
        elif username in userlist:
            return False, "Username already taken"

        else:
            return True, f"Successfully added \"{username}\" to database"

    def remove_task_from_db(self, id, task):
        deletion_criteria = {
            "userID": id,
            "task": task
        }
        try:
            self.todo_collection.delete_one(deletion_criteria)
            return 1
        except:
            return 0
