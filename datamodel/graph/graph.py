

class WeightedGraph:

    def __init__(self):
        self.vertices = {}

    def addVertex(self, data: str, weights: list):
        new_id = len(self.vertices) + 1
        self.vertices[new_id] = (data, weights)

    def getGraph(self):
        return self.vertices

    def __str__(self):
        string = ""
        for i in self.vertices:
            string +=  str(i) + ": " + str(self.vertices[i]) + "\n"
        return string

