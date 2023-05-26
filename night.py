from datetime import datetime
from database import MongoDB

class Night:
    def __init__(self, data):
        self.data_values = data # [weight(kg),walking(1-5),exercise(1-5),learn(1-5),read(1-5),
                         # meditation(true/false), ifast(true/false)]

        self.data_keys = ["weight", "walking", "exercise", "learning", "reading", "meditation", "ifast"]

        # combine keys and values from lists into a dict
        self.data = {key: value for key, value in zip(self.data_keys, self.data_values)}

        # get date and time
        self.today = str(datetime.now().date())
        self.time = str(datetime.now().time().strftime("%H:%M"))

        # set database
        self.db = MongoDB()
        self.db.connect_to_localhost()

        # add extra attributes to the data and send to DB
        return_data = {
            "date": self.today,
        }
        return_data.update(self.data)
        if self.db.data_collection.find_one({"date":self.today}):
            self.db.data_collection.update_one({"date":self.today}, {'$set':return_data})
        else:
            self.db.add_data("data_collection", return_data)

        # add todays bedtime to database
        bedtime_data = {"date":self.today, "bedtime": self.time}
        if self.db.bedtime_collection.find_one({"date":self.today}):
            self.db.bedtime_collection.update_one({"date":self.today},{'$set':bedtime_data})

        else:
            self.db.add_data("bedtime_collection", bedtime_data)
