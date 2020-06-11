

class Truck:

    MAX_DISTANCE = 145

    def __init__(self):
        self.packages = 0
        self.route = []
        self.speed = 18

    def set_route(self, route):
        self.route = route
