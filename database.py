from pymongo import MongoClient
from datetime import datetime, timedelta

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect_to_localhost(self, database_name="localhost", collection_name=27017):
        self.client = MongoClient(database_name, collection_name)
        # Choose database
        self.db = self.client.myappDB
        # Choose collection
        self.data_collection = self.db.data_collection
        self.todo_collection = self.db.todo_collection
        self.bedtime_collection = self.db.bedtime_collection
        self.wutime_collection = self.db.wutime_collection

    def add_data(self, collection, data):
        if collection == "data_collection":
            self.data_collection.insert_one(data)
        elif collection == "todo_collection":
            self.todo_collection.insert_one(data)
        elif collection == "bedtime_collection":
            self.bedtime_collection.insert_one(data)
        elif collection == "wutime_collection":
            self.wutime_collection.insert_one(data)

    def get_bedtime(self):
        # find yesterday bedtime
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        query = {yesterday: {'$exists': True}}
        time = list(self.bedtime.find_one(query).items())[-1][-1]
        return time

    def get_todo_list(self):
        todolist = self.todo_collection.find({}, {"_id": 0})
        todolist = list(todolist)
        return todolist

#mongo = mongodb.MongoDB()
#mongo.connect_to_localhost()
#mongo.add_new_player("player_data")
#list_of_players = mongo.get_list_of_players()