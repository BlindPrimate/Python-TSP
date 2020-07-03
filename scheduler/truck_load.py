from globals import *


class TruckLoad:
    def __init__(self, packages):
        self.packages = packages
        self.regular_packages = []
        self.priority_packages = []
        self.truck_loads = []

        # give truck some empty space to except special packages on routes
        self.effective_truck_capacity = int(round(TRUCK_CAPACITY - TRUCK_CAPACITY * 0.2))
        self.special_packages = {
            "truck": [],
            "delayed": [],
            "deliver_with": [],
            "wrong_address": [],
        }

        # package sorting
        self.packages.sort(key=lambda x: (x.deadline, x.address))
        self._sort_packages()

        # package consolidation

    def _sort_packages(self):
        address_clusters = {}

        # sort priority, special, and regular packages
        for package in self.packages:
            if package.has_special_status():
                special = package.get_special_status()
                self.special_packages[special].append(package)
            elif package.deadline != END_OF_DAY:
                self.priority_packages.append(package)
            else:
                self.regular_packages.append(package)

        all_loads = self.priority_packages + self.regular_packages
        self.truck_loads = self._load_split(all_loads)

    def _load_split(self, packages):
        result = []
        count = 0
        while count <= len(packages):
            # check if previous loads are to full effective truck capacity -- fill if not
            if result:
                for load in result:
                    if len(load) < self.effective_truck_capacity:
                        space_remaining = self.effective_truck_capacity - len(load)
                        while space_remaining:
                            load.append(packages[count])
                            count += 1
                            space_remaining -= 1

            # cut sorted_packages into spans of TRUCK_CAPACITY size
            if count + self.effective_truck_capacity == len(packages):
                break
            if count + self.effective_truck_capacity > len(packages):
                result.append(packages[count:])
                count += self.effective_truck_capacity
            else:
                result.append(packages[count:count + self.effective_truck_capacity])
                count += self.effective_truck_capacity
        return result


