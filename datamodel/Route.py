from datamodel.io import CSVImport
from sys import maxsize
from globals import TRUCK_SPEED

import datetime

class Route:
    def __init__(self, route_stops, packages):
        csv = CSVImport()
        self.distance_table = csv.import_distances()
        self.route = self._optimize_route(route_stops)
        self.packages = packages



    def _optimize_route(self, route_stops):
        # clear duplicates
        route = []
        [route.append(i) for i in route_stops if i not in route]

        # always start at hub
        start_vert = 0
        optimized_route = [start_vert]

        # continue until all vertices have been added to the route
        while len(optimized_route) <= len(route):
            best_edge = maxsize
            best_vert = 0

            # compare against other vertices
            for vert in route:
                # ignore verts that have already been added to routes
                if vert in optimized_route or vert == start_vert:
                    continue
                edge_weight = float(self.distance_table[start_vert][vert])
                if edge_weight < best_edge:
                    best_edge = edge_weight
                    best_vert = vert
                    start_vert = vert

            optimized_route.append(best_vert)
        return optimized_route

    def total_route_distance(self) -> float:
        total = 0
        # cycle through stop locations stop -> stop 2(stop + 1) -> stop 3(stop + 1 + 1)  -> etc
        for index, value in enumerate(self.route):
            start = value
            # break when end of list reached
            if index == len(self.route) - 1:
                # add trip back to hub
                total += float(self.distance_table[start][0])
                break
            end = self.route[index + 1]
            total += float(self.distance_table[start][end])

        return total

    def total_route_time(self) -> float:
        distance = self.total_route_distance()
        return distance / TRUCK_SPEED


    def __len__(self):
        return len(self.route)

    def __repr__(self):
        return "Route: " + str(self.route)

    def __str__(self):
        return "Route: " + str(self.route)

    def __eq__(self, obj):
        if isinstance(obj, list):
            for i in range(len(self.route)):
                if self.route[i] != obj[i]:
                    return False
            return True
