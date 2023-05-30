from database import MongoDB
from datetime import datetime

class Morning:
    def __init__(self, id):
        # get date and time
        self.today = str(datetime.now().date())
        self.time = str(datetime.now().time().strftime("%H:%M"))

        # set database
        self.db = MongoDB()
        self.db.connect_to_localhost()

        # add wake up time to db
        wutime_data = {"userID":id, "date":self.today, "time": self.time}
        if not self.db.wutime_collection.find_one({"userID":id, "date":self.today}):
            self.db.add_data("wutime_collection", wutime_data)

        self.todays_wakeup_time = self.db.get_wakeup_time(id)


