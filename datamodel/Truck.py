from globals import *

class Truck:

    def __init__(self, id):
        self.id = id
        self.route = []
        self.packages = []
        self.speed = 18
        self.next_available = START_OF_DAY

    def is_truck_available(self, time_of_day):
        return self.next_available <= time_of_day

    def set_route(self, route):
        self.route = route

    def truck_departing_hub(self):
        for stop in self.route:
            for package in stop.packages:
                package.status = ON_ROUTE

    def truck_returning_hub(self, time_of_day):
        self.next_available = time_of_day
        self.route = []
