import datamodel.io as io
from datamodel.hashtable import HashTable
from datamodel.graph import WeightedGraph

if __name__ == "__main__":
    data = io.CSVImport()
    distances = data.import_distances()
    packages = data.import_packages()
    graph_distances = WeightedGraph()
    hash_packages = HashTable(50)

    for i in distances:
        data = i[1] + i[2]
        weights = i[3:]
        graph_distances.addVertex(data, weights)

    print(graph_distances)

    # for i in packages:
    #     hash_packages.insert(i)

    # print(hash_packages)
