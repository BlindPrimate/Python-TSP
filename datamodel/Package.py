
import datetime

class Package:

    def __init__(self, id, address, city, state, zip, deadline, mass, status, *special):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        if deadline == "EOD":
            self.deadline = datetime.datetime.strptime("5:30 pm", "%I:%M %p")
        else:
            self.deadline = datetime.datetime.strptime(deadline, "%I:%M %p")
        self.mass = mass
        self.status = status
        self.special = special


