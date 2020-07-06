from globals import *
from itertools import groupby


class TruckLoad:
    def __init__(self, packages):
        self.packages = packages
        self.regular_packages = []
        self.priority_packages = []
        self.truck_loads = []

        # give truck some empty space to except special packages on routes
        self.effective_truck_capacity = int(round(TRUCK_CAPACITY - TRUCK_CAPACITY * 0.1))
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

        # split packages into groups of packages based on address
        self.priority_packages = [list(i) for j, i in groupby(self.priority_packages, lambda x: x.address)]
        self.regular_packages = [list(i) for j, i in groupby(self.regular_packages, lambda x: x.address)]

        package_clusters = self.priority_packages + self.regular_packages
        self.truck_loads = self._load_split(package_clusters)

    def _load_split(self, package_clusters):
        result = []
        load = []
        for cluster in package_clusters:
            if len(load) >= self.effective_truck_capacity:
                result.append(load)
                load = []

            if len(load) + len(cluster) <= self.effective_truck_capacity:
                load += cluster
            else:
                result.append(load)
                load = [cluster]
        else:
            if load:
                result.append(load)
        return result



