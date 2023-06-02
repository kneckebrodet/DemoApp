from kivy.uix.image import CoreImage
import io
import matplotlib.pyplot as plt
import numpy as np
from database import MongoDB

class Graph:
    def __init__(self, app, id, dates, targets):
        self.db = MongoDB()
        self.db.connect_to_localhost()
        self.app = app
        self.id = id
        self.dates = dates
        self.targets = targets
        self.active_dates = []

        self.create_first_graph()

        if not self.targets:
            self.app.root.get_screen("graph").ids.img2.texture = None
        else:
            self.create_second_graph()

    def create_first_graph(self):
        plt.clf()
        ## Remove dates without stats and create two lists: [active dates], [[date_stats], x4]
        all_records = []
        for date in self.dates:
            self.date_has_obj = False
            date_stats = []
            try:
                date_stats.append(self.db.data_collection.find_one({"userID":self.id, "date":date})["sleep"])
                date_stats.append(self.db.data_collection.find_one({"userID":self.id, "date":date})["weight"])
                #date_stats.append(db.data_collection.find_one({"userID":id, "date":date})["meditaion"])
                #date_stats.append(db.data_collection.find_one({"userID":id, "date":date})["ifast"])
                self.date_has_obj = True
            except:
                continue
            if self.date_has_obj:
                self.active_dates.append(date)
                all_records.append(date_stats)


        ## Check if data in database
        if len(all_records) < 2:
            pass
        else:
            ## Sort the stats by category instead of date: (0)sleep -> (1)weight -> (2)meditation -> (3)ifast
            records_by_cat = [list(row) for row in zip(*all_records)]
            ## Converting the format from: "6:30" => 6.50, (sleep records)
            for index, record in enumerate(records_by_cat[0]):
                record = record.split(":")
                record = list(map(int, record))
                record[1] = round(record[1] / 60, 2)

                records_by_cat[0][index] = record[0] + record[1]

            ## Converting the format from: "70.0" => 7.00, (weight records)
            for index, record in enumerate(records_by_cat[1]):
                records_by_cat[1][index] = round(float(record) / 10, 2)

            ## Create the Graph
            plt.clf()

            ## change the format of the date (x axis) from : 2023-05-29 => 23/05/29 for cleaner look
            x = []
            for index, date in enumerate(self.active_dates):
                x.append(str(self.active_dates[index]).replace("-","/")[2:])

            for y in records_by_cat:
                plt.plot(x, y)

            plt.legend(["Sleep", "Weight"])
            plt.title("")

            plt.ylim(0, 15)

            if len(self.active_dates) > 10:
                plt.xticks(np.arange(0, len(self.active_dates), len(self.active_dates)//10))

            plt.xticks(rotation='vertical')
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf)

            buf.seek(0)
            self.app.root.get_screen("graph").ids.img1.texture = CoreImage(buf, ext="png").texture
            del buf

    def create_second_graph(self):
        ## get all the targets and dates
        plt.clf()
        all_records = []
        dates = []
        for date in self.active_dates:
            stats = []
            self.date_has_obj = False
            for target in self.targets:
                try:
                    stats.append(self.db.data_collection.find_one({"userID":self.id, "date":date})[target])
                    self.date_has_obj = True
                except:
                    continue
            if self.date_has_obj:
                all_records.append(stats)
                dates.append(date)

        ## Sort the stats by category instead of date
        records_by_cat = [list(row) for row in zip(*all_records)]

        ## Draw graph
        plt.clf()
        x = []
        for index, date in enumerate(self.active_dates):
            x.append(str(self.active_dates[index]).replace("-","/")[2:])

        for y in records_by_cat:
            plt.bar(x, y)

        plt.legend(self.targets)
        plt.title("")

        if len(dates) > 10:
            plt.xticks(np.arange(0, len(dates), len(dates)//10))

        plt.xticks(rotation='vertical')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf)

        buf.seek(0)
        self.app.root.get_screen("graph").ids.img2.texture = CoreImage(buf, ext="png").texture
        del buf