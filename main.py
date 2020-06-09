import datamodel.io as io
from datamodel.hashtable import HashTable
from datamodel.graph import WeightedGraph
from datamodel import Package

def build_graph(graph_data):
    graph = WeightedGraph()
    for i in graph_data:
        data = i[1] + i[2]
        weights = i[3:]
        graph.addVertex(data, weights)
    return graph

def build_package_table(package_data):
    hash_table = HashTable(50)

    for package in package_data:
        # unpack csv provided list to variables
        id, address, city, state, zip, deadline, mass, special = package[:8]
        # build package object
        package = Package(id, address, city, state, zip, deadline, mass)
        # insert into hash table with provided id for easier retrieval
        hash_table.insert(package, id)
    return hash_table



if __name__ == "__main__":
    data = io.CSVImport()
    distances = data.import_distances()
    packages = data.import_packages()
    graph_distances = build_graph(distances)
    hash_packages = build_package_table(packages)



