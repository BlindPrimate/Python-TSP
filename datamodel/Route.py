from datamodel.io import CSVImport
from globals import TRUCK_SPEED

class RoutePoint:
    def __init__(self, address_id: int, packages: list):
        self.address_id = address_id
        self.packages = packages
        self.distance_to = 0
        self.travel_time = 0

    def _set_travel_time(self, distance):
        self.travel_time = distance / TRUCK_SPEED

    def set_distance_to(self, distance):
        self.distance_to = distance
        self._set_travel_time(distance)

    def __eq__(self, other):
        if self.address_id == other.address_id:
            return True
        return False

    def __repr__(self):
        return "RoutePoint: ({}, {})".format(self.address_id, self.packages)

    def __str__(self):
        return "RoutePoint: ({}, {})".format(self.address_id, self.packages)


class Route:
    def __init__(self, route=None):
        if route is None:
            route = []
        csv = CSVImport()
        self.route_stops = route
        self.distance_table = csv.import_distances()

    def add_stop(self, stop):
        self.route_stops.append(stop)

    def get_address_indexes(self):
        return [i.address_id for i in self.route_stops]

    def total_route_distance(self) -> float:
        total = 0.0
        for stop in self.route_stops:
            total += stop.distance_to
        return total

    def total_route_time(self) -> float:
        distance = self.total_route_distance()
        return distance / TRUCK_SPEED

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
        if self.route_stops == obj.route_stops:
            return True
        return False
