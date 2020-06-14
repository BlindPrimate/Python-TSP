import datetime

import datamodel.io as io
from datamodel.hashtable import HashTable
from datamodel import Package
from scheduling import Scheduler

from globals import *






if __name__ == "__main__":

    # print(graph_distances)
    scheduler = Scheduler()

    routes = [route for route in scheduler.route_generator()]
    depart = datetime.time(9, 0, 0)
    for i in routes:
        pass
        # scheduler.build_route_schedule(i, depart)






