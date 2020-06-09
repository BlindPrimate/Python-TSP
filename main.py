import datamodel.io as io
from datamodel.hashtable import HashTable

if __name__ == "__main__":
    data = io.CSVImport()
    distances = data.import_distances()
    packages = data.import_packages()
    hash = HashTable(100)

    for i in distances:
        hash.insert(i)

    print(hash)
