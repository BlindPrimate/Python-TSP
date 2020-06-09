
class Package:

    def __init__(self, id, address, city, state, zip, deadline, mass, status, *special):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.status = status
        self.special = special


