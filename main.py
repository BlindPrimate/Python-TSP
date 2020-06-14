import datetime

import datamodel.io as io
from datamodel.hashtable import HashTable
from datamodel import Package
from scheduling import Scheduler

from globals import *






if __name__ == "__main__":

    # print(graph_distances)
    scheduler = Scheduler()

    scheduler.regular_route_builder()
    scheduler.special_route_builder()
    # print("regular")
    for route in scheduler.regular_routes:
        pass
    for i in scheduler.special_routes:
        pass

    depart = datetime.time(9, 0, 0)






