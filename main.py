import datetime

import datamodel.io as io
from datamodel.hashtable import HashTable
from datamodel import Package
from scheduling import Scheduler

from globals import *






if __name__ == "__main__":

    # print(graph_distances)
    scheduler = Scheduler()

    scheduler.route_builder()
    for i in scheduler.regular_routes:
        print(i)
    depart = datetime.time(9, 0, 0)






