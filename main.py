import datetime
from scheduling import Scheduler

from globals import *


if __name__ == "__main__":

    # print(graph_distances)
    scheduler = Scheduler()

    scheduler.regular_route_builder()
    scheduler.special_route_builder()

    for route in scheduler.regular_routes:
        sched_1 = scheduler.build_route_schedule(route)
        for i in sched_1:
            print(i)
    # print("regular")


    depart = datetime.time(9, 0, 0)






