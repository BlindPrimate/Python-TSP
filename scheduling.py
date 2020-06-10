from globals import *

class Scheduler:

    def __init__(self, package_data):
        self.schedule = []
        self.raw_data = package_data


    def route_builder(self):
        pass


    def _truck_load_builder(self):
        sorted_packages = self._sort_packages()
        truck_loads = []
        count = 0
        # cut sorted_packages into spans of TRUCK_CAPACITY size
        while count <= len(sorted_packages):
            if count + TRUCK_CAPACITY > len(sorted_packages):
                truck_loads.append(sorted_packages[count:])
            else:
                truck_loads.append(sorted_packages[count:count + TRUCK_CAPACITY])
            count += TRUCK_CAPACITY
        return truck_loads

    def _sort_packages(self):
        package_list = self.raw_data.to_list()
        # sort packages by deadline time
        package_list.sort(key=lambda package: package.deadline)
        return package_list



