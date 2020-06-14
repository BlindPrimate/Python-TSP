import datetime

class Package:

    def __init__(self, id, address, city, state, zip, deadline, mass, status, *special):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.address_index = None
        if deadline == "EOD":
            self.deadline = datetime.datetime.strptime("5:30 pm", "%I:%M %p")
        else:
            self.deadline = datetime.datetime.strptime(deadline, "%I:%M %p")
        self.mass = mass
        self.status = status
        self.special = {
            "truck": None,
            "delayed": None,
            "deliver_with": None,
            "wrong_address": False,
        }

    def get_special_status(self):
        for key, value in self.special.items():
            if value:
                return key

    def has_special_status(self):
        return any(self.special.values())

    def set_special_status(self, status):
        if status == "Can only be on truck 2":
            self.special["truck"] = 2
        elif status == "Delayed on flight---will not arrive to depot until 9:05 am":
            self.special["delayed"] = datetime.time(9, 5, 0)
        elif status == "Wrong address listed":
            self.special["wrong_address"] = True
        elif status == "Must be delivered with 15, 19":
            self.special["deliver_with"] = [15, 19]
        elif status == "Must be delivered with 13, 19":
            self.special["deliver_with"] = [13, 19]
        elif status == "Can only be on truck 2":
            self.special["truck"] = 2
        elif status == "Must be delivered with 13, 15":
            self.special["deliver_with"] = [13, 15]
        elif status == "Delayed on flight---will not arrive to depot until 9:05 am":
            self.special["delayed"] = datetime.time(9, 5, 0)
        elif status == "Can only be on truck 2":
            self.special["truck"] = 2

    def package_details(self):
        return "{}   {}. {}, {}., {}  {}  {}  {}".format(self.id,
                                                         self.address,
                                                        self.city,
                                                        self.state,
                                                        self.zip,
                                                        self.deadline.time(),
                                                        self.mass,
                                                        self.status,
                                                        self.special
                                                        )
