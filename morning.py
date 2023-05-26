from database import MongoDB
from datetime import datetime

class Morning:
    def __init__(self):
        # get date and time
        self.today = str(datetime.now().date())
        self.time = str(datetime.now().time().strftime("%H:%M"))

        # set database
        self.db = MongoDB()
        self.db.connect_to_localhost()

        # add wake up time to db
        wutime_data = {"date":self.today, "bedtime": self.time}
        if not self.db.wutime_collection.find_one({"date":self.today}):
            self.db.add_data("wutime_collection", wutime_data)



