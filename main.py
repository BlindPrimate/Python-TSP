import datamodel.io as io
from datamodel.hashtable import HashTable
from datamodel.graph import WeightedGraph
from datamodel import Package
from scheduling import Scheduler
from datamodel import Truck
from globals import *




def build_graph(graph_data):
    graph = WeightedGraph()
    for i in graph_data:
        data = i[1] + i[2]
        weights = i[3:]
        graph.addVertex(data, weights)
    return graph

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
    graph_distances = build_graph(distances)
    hash_packages = build_package_table(packages)

    # print(graph_distances)
    scheduler = Scheduler(hash_packages)
    routes = scheduler.route_generator()
    trucks = []
    for route in routes:
        truck = Truck()
        truck.packages = route
        trucks.append(truck)




