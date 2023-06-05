
from database import MySQL
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

class Graph:
    def __init__(self, app, id, dates, targets):
        self.app = app
        self.id = id
        self.dates = dates
        self.targets = targets
        self.recorded_dates = []

        self.create_first_graph()
        if self.targets:
            self.create_second_graph()


    ### FIRST GRAPH ( WEIGHT SLEEP )
    def create_first_graph(self):
        ## Remove dates without stats and create two lists: [active dates], [[date_stats], x4]
        all_records = []
        self.db = MySQL()
        for date in self.dates:
            self.date_has_obj = False
            date_stats = []
            try:
                date_stats.append(self.db.get_stat(self.id, date, "sleep"))
                date_stats.append(self.db.get_stat(self.id, date, "weight"))
                #date_stats.append(db.data_collection.find_one({"userID":id, "date":date})["meditaion"])
                #date_stats.append(db.data_collection.find_one({"userID":id, "date":date})["ifast"])
                self.date_has_obj = True
            except:
                continue
            if self.date_has_obj:
                self.recorded_dates.append(date)
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

            fig, ax = plt.subplots()
            canvas = fig.canvas

            ## change the format of the date (x axis) from : 2023-05-29 => 23/05/29 for cleaner look
            x = []
            for index, date in enumerate(self.recorded_dates):
                x.append(str(self.recorded_dates[index]).replace("-","/")[2:])

            for y in records_by_cat:
                ax.plot(x,y)

            plt.legend(["Sleep", "Weight"])
            plt.ylim(0, 15)
            if len(self.recorded_dates) > 10:
                plt.xticks(np.arange(0, len(self.recorded_dates), len(self.recorded_dates)//10))
            
            plt.xticks(rotation='vertical')
            plt.tight_layout()

            canvas = FigureCanvasKivyAgg(plt.gcf())
            self.app.root.get_screen("graph").ids.bx1.add_widget(canvas)

            
    ### SECOND GRAPH ( CHECKED BOXES )
    def create_second_graph(self):
        ## get all the targets and dates
        all_records = []
        dates = []
        for date in self.recorded_dates:
            stats = []
            self.date_has_obj = False
            for target in self.targets:
                try:
                    stats.append(self.db.get_stat(self.id,date, target))
                    self.date_has_obj = True
                except:
                    continue
            if self.date_has_obj:
                all_records.append(stats)
                dates.append(date)

        ## Sort the stats by category instead of date
        records_by_cat = [list(row) for row in zip(*all_records)]
        ## Draw graph
        fig, ax = plt.subplots()
        canvas = fig.canvas
        x = []

        for index, date in enumerate(self.recorded_dates):
            x.append(str(self.recorded_dates[index]).replace("-","/")[2:])
        
        bottom_values = [0] * len(x)  # Initialize the bottom values for stacking the bars

        for y in records_by_cat:
            ax.bar(x, y, bottom=bottom_values)  # Stack the bars from the bottom values
            bottom_values = [b + h for b, h in zip(bottom_values, y)]

        plt.legend(self.targets)

        if len(dates) > 10:
            plt.xticks(np.arange(0, len(dates), len(dates)//10))

        plt.xticks(rotation='vertical')
        plt.tight_layout()

        canvas = FigureCanvasKivyAgg(plt.gcf())
        self.app.root.get_screen("graph").ids.bx2.add_widget(canvas)
