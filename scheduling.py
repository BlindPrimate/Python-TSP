from globals import *
from sys import maxsize

class Scheduler:

    def __init__(self, package_data):
        self.raw_data = package_data

    def cycle_finder(self, distance_table:list, cycle_path:list):

        # always start at hub
        start_vert = 0
        route = [start_vert]

        while len(route) <= len(cycle_path):
            best_edge = maxsize
            best_vert = 0

            for vert in cycle_path:
                if vert in route or vert == start_vert:
                    continue
                print(distance_table[start_vert])
                edge_weight = float(distance_table[start_vert][vert])
                if edge_weight < best_edge:
                    best_edge = edge_weight
                    best_vert = vert
                    start_vert = vert

            route.append(best_vert)
        return route

















    def route_builder(self):
        for truck_load in self._truck_load_generator():
            package_stops = [package.address for package in truck_load]
            truck_route = []




    def _truck_load_generator(self):
        sorted_packages = self._sort_packages()
        count = 0
        # cut sorted_packages into spans of TRUCK_CAPACITY size
        while count <= len(sorted_packages):
            if count + TRUCK_CAPACITY > len(sorted_packages):
                yield sorted_packages[count:]
            else:
                yield sorted_packages[count:count + TRUCK_CAPACITY]
            count += TRUCK_CAPACITY

    def _sort_packages(self):
        package_list = self.raw_data.to_list()
        # sort packages by deadline time
        package_list.sort(key=lambda package: package.deadline)
        return package_list



