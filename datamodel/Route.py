from datamodel.io import CSVImport
from sys import maxsize
from globals import TRUCK_SPEED

import datetime

class RoutePoint:
    def __init__(self, address_id: int, packages: list):
        self.address_id = address_id
        self.packages = packages
        self.distance_to = 0
        self.travel_time = 0

    def set_travel_time(self, time):
        self.travel_time = time

    def set_distance_to(self, distance):
        self.distance_to = distance

    def __repr__(self):
        return "RoutePoint: ({}, {})".format(self.address_id, self.packages)

    def __str__(self):
        return "RoutePoint: ({}, {})".format(self.address_id, self.packages)

class Route:
    def __init__(self, route=None):
        if route is None:
            route = []
        self.route_stops = route
        csv = CSVImport()
        self.distance_table = csv.import_distances()

    def add_stop(self, stop):
        self.route_stops.append(stop)

    def get_address_indexes(self):
        return [i.address_id for i in self.route_stops]

    # def total_route_distance(self) -> float:
    #     total = 0
    #     # cycle through stop locations stop -> stop 2(stop + 1) -> stop 3(stop + 1 + 1)  -> etc
    #     for index, value in enumerate(self.route_stops):
    #         start = value.address_id
    #         # break when end of list reached
    #         if index == len(self.route_stops) - 1:
    #             # add trip back to hub
    #             total += float(self.distance_table[start][0])
    #             break
    #         end = self.route_stops[index + 1].address_id
    #         total += float(self.distance_table[start][end])
    #     return total
    #
    # def total_route_time(self) -> float:
    #     distance = self.total_route_distance()
    #     return distance / TRUCK_SPEED

    def __len__(self):
        return len(self.route_stops)

    def __getitem__(self, item):
        return self.route_stops[item]

    def __repr__(self):
        return "Route: " + str(self.route_stops)

    def __str__(self):
        return "Route: " + str(self.route_stops)

    def __iter__(self):
        for stop in self.route_stops:
            yield stop

    def __eq__(self, obj):
        if isinstance(obj, list):
            for i in range(len(self.route_stops)):
                if self.route_stops[i] != obj[i]:
                    return False
            return True
