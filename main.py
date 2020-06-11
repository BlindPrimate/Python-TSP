import datamodel.io as io
from datamodel.hashtable import HashTable
from datamodel import Package
from scheduling import Scheduler
from datamodel import Route
from datamodel import Truck

from globals import *





def build_package_table(package_data):
    hash_table = HashTable(45)

    for package in package_data:
        if package[0]:
            # print(package[0])
            # unpack csv provided list to variables
            id, address, city, state, zip, deadline, mass, special = package[:8]
            # build package object
            package = Package(id, address, city, state, zip, deadline, AT_HUB, mass)
            # insert into hash table with provided id for easier retrieval
            hash_table.insert(package, id)
    return hash_table



if __name__ == "__main__":
    data = io.CSVImport()
    distances = data.import_distances()
    packages = data.import_packages()
    hash_packages = build_package_table(packages)

    # print(graph_distances)
    scheduler = Scheduler(hash_packages)
    trucks = []
    for route in scheduler.route_generator():
        truck = Truck()
        truck.set_route(Route(route))
        trucks.append(truck)

    for truck in trucks:
        print(truck.route.total_route_distance())
    # simulate routes




