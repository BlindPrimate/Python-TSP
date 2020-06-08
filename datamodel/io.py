import csv
import os

_WORKING_PATH = os.path.dirname(os.path.abspath(__file__))


class CSVImport:
    def __init__(self):
        self.package_data = self._import_packages()
        self.distances = self._import_distances()

    def _import_packages(self):
        packages_url = os.path.join(_WORKING_PATH, "data/packages.csv")
        with open(packages_url, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data

    def _import_distances(self):
        distances_url = os.path.join(_WORKING_PATH, "data/distances.csv")
        with open(distances_url, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data

    def get_hash_table(self):
        for i in self.distances:
            print(i)

