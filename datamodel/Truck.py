from globals import *

class Truck:

    MAX_DISTANCE = 145

    def __init__(self, id):
        self.id = id
        self.route = []
        self.speed = 18
        self.isAvailable = True

    def set_route(self, route):
        self.route = route

    def truck_departing_hub(self):
        self.isAvailable = False
        for stop in self.route:
            for package in stop.packages:
                package.status = ON_ROUTE

    def truck_returning_hub(self):
        self.isAvailable = True
        self.route = []
