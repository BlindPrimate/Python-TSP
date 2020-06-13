

class RoutePoint:
    def __init__(self, address_id: int, packages: list):
        self.address_id = address_id
        self.packages = packages

    def __repr__(self):
        return "RoutePoint: ({}, {})".format(self.address_id, self.packages)

    def __str__(self):
        return "RoutePoint: ({}, {})".format(self.address_id, self.packages)
