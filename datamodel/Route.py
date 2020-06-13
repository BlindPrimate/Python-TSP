from datamodel.io import CSVImport
from sys import maxsize
from globals import TRUCK_SPEED
from datamodel.RoutePoint import RoutePoint

import datetime

class Route:
    def __init__(self, route_stops):
        csv = CSVImport()
        self.distance_table = csv.import_distances()
        self.route_stops = self._optimize_route(route_stops)

    def get_address_indexes(self):
        return [i.address_id for i in self.route_stops]

    def _consolidate_stops(self, route_stops):
        """
        Consolidates any packages going to stops that appear twice in a route.
        :param route_stops:
        :return: list
        """
        consolidated = []
        used = []
        for stop in route_stops:
            # if stop has only one package send to consolidated list
            if stop.address_id not in used:
                consolidated.append(stop)
                used.append(stop.address_id)
            # else look for package with identical address and add package to it
            else:
                for consolidated_stop in consolidated:
                    if consolidated_stop.address_id == stop.address_id:
                        consolidated_stop.packages.extend(stop.packages)
        return consolidated

    def _optimize_route(self, route_stops):
        # clear duplicates
        route = self._consolidate_stops(route_stops)
        print(route)

        # always start at hub
        start_delivery_point = RoutePoint(0, None)
        optimized_route = [start_delivery_point]

        # continue until all vertices have been added to the route
        while len(optimized_route) <= len(route):
            best_edge = maxsize
            best_delivery_point = 0

            # compare against other delivery points
            for delivery_point in route:
                # ignore delivery points that have already been added to optimized route
                if delivery_point in optimized_route or delivery_point == start_delivery_point:
                    continue
                edge_weight = float(self.distance_table[start_delivery_point.address_id][delivery_point.address_id])
                if edge_weight < best_edge:
                    best_edge = edge_weight
                    best_delivery_point = delivery_point
                    start_delivery_point = delivery_point

            optimized_route.append(best_delivery_point)
        return optimized_route

    def total_route_distance(self) -> float:
        total = 0
        # cycle through stop locations stop -> stop 2(stop + 1) -> stop 3(stop + 1 + 1)  -> etc
        for index, value in enumerate(self.route_stops):
            start = value.address_id
            # break when end of list reached
            if index == len(self.route_stops) - 1:
                # add trip back to hub
                total += float(self.distance_table[start][0])
                break
            end = self.route_stops[index + 1].address_id
            total += float(self.distance_table[start][end])

        return total

    def total_route_time(self) -> float:
        distance = self.total_route_distance()
        return distance / TRUCK_SPEED




    def __len__(self):
        return len(self.route_stops)

    def __repr__(self):
        return "Route: " + str(self.route_stops)

    def __str__(self):
        return "Route: " + str(self.route_stops)

    def __eq__(self, obj):
        if isinstance(obj, list):
            for i in range(len(self.route_stops)):
                if self.route_stops[i] != obj[i]:
                    return False
            return True
