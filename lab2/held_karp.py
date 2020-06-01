import math
import os
import sys
from threading import Timer
import time

PI = 3.141592
RRR = 6378.388
stop = False

def timeover():
    global stop
    stop = True

class Node():

    def __init__(self, name, latitude, longitude):
        self._name = name
        self._visited = False
        self._edges = []
        self._latitude = latitude
        self._longitude = longitude

    def __gt__(self, other):
        return self._name > other._name

    def __lt__(self, other):
        return self._name < other._name

    def __le__(self, other):
        return self._name <= other._name

    def __ge__(self, other):
        return self._name >= other._name

    def __eq__(self, other):
        return self._name == other._name

    def __ne__(self, other):
        return self._name != other._name

    def __repr__(self):
        return str(self._name+1)

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def visited(self):
        return self._visited

    def set_visited(self, visited):
        self._visited = visited

    def edges(self):
        return self._edges

    def add_edge(self, edge):
        self._edges.append(edge)

    def remove_edge(self, edge):
        del self._edges[-1]

    def latitude(self):
        return self._latitude

    def latitude_rad(self):
        deg = int(self._latitude)
        rounded = self._latitude - deg
        return PI * (deg + 5.0 * (rounded / 3.0)) / 180.0

    def set_latitude(self, latitude):
        self._latitude = latitude

    def longitude(self):
        return self._longitude

    def longitude_rad(self):
        deg = int(self._longitude)
        rounded = self._longitude - deg
        return PI * (deg + 5.0 * (rounded / 3.0)) / 180.0

    def set_longitude(self, longitude):
        self._longitude = longitude

    def find_edge(self, dest):
        for i, val in enumerate(self._edges):
            if val.opposite(self) == dest:
                return val


class Edge():

    def __init__(self, src, dest, weight):
        self._nodes = src, dest
        self._weight = weight
        self._label = None

    def __gt__(self, other):
        return self._weight > other._weight

    def __lt__(self, other):
        return self._weight < other._weight

    def __le__(self, other):
        return self._weight <= other._weight

    def __ge__(self, other):
        return self._weight >= other._weight

    def __eq__(self, other):
        return self._weight == other._weight

    def __ne__(self, other):
        return self._weight != other._weight

    def __str__(self):
        return self._weight

    def weight(self):
        return self._weight

    def nodes(self):
        return self._nodes

    def label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    def opposite(self, node):
        if node == self._nodes[0]:
            return self._nodes[1]
        if node == self._nodes[1]:
            return self._nodes[0]
        return None


# %%


class Graph():

    def __init__(self, n):
        self._nodes = [None] * n
        self._edges = []

    def add_node(self, name, latitude, longitude):
        if not self.is_node_present(name):
            node = Node(name, latitude, longitude)
            self._nodes[name] = node
            return node
        else:
            return self._nodes[name]

    def add_edge(self, src, dest, weight):
        edge = Edge(src, dest, weight)
        self._edges.append(edge)
        self._nodes[src.name()].add_edge(edge)
        self._nodes[dest.name()].add_edge(edge)

    def get_edges(self):
        return self._edges

    def get_nodes(self):
        return self._nodes

    def is_node_present(self, name):
        if self._nodes[name] is None:
            return False
        else:
            return True

    def num_vertici(self):
        return len(self._nodes)

    def remove_edge(self, edge):
        self._edges.pop()
        self._nodes[edge._nodes[0]._name].remove_edge(edge)
        self._nodes[edge._nodes[1]._name].remove_edge(edge)

    def geo_distance(self, src, dest):
        q1 = math.cos(src.longitude_rad() - dest.longitude_rad())
        q2 = math.cos(src.latitude_rad() - dest.latitude_rad())
        q3 = math.cos(src.latitude_rad() + dest.latitude_rad())
        return int(RRR * math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)

    def euclide_distance(self, src, dest):
        x = abs(src.latitude() - dest.latitude())
        y = abs(src.longitude() - dest.longitude())
        return int(math.sqrt(math.pow(x, 2)+math.pow(y, 2)))


"""
v = nodo
S = lista di vertici
d_dict = dizionario: indici [n, str(S)]
p_dict = dizionario: indici [n, str(S)]
"""


def held_karp(start, v, S: list, d_dict, p_dict):
    global stop
    if len(S) == 1 and v in S:
        return v.find_edge(start).weight()
    elif (str(v.name()+1), str(S)) in d_dict:
        return d_dict[(str(v.name()+1), str(S))]
    else:
        mindist = float("Inf")
        minprec = None
        S2 = list(S)
        S2.remove(v)
        for i in range(len(S2)):
            dist = held_karp(start, S2[i], S2, d_dict, p_dict)
            uv_weight = S2[i].find_edge(v).weight()
            if(dist + uv_weight < mindist):
                mindist = dist + uv_weight
                minprec = S2[i]
            if stop:
                break
        d_dict[(str(v.name()+1), str(S))] = mindist
        p_dict[(str(v.name()+1), str(S))] = minprec
        return mindist


def read_file(filename):
    file = open(filename, "r")
    type = ""
    vertici = 0

    while True:
        line = file.readline()
        line = line.replace(" :", ":")
        if "NODE_COORD_SECTION" in line:
            break
        label, value = list(line.split(maxsplit=1))
        if "EDGE_WEIGHT_TYPE" in label:
            type = value
        if "DIMENSION" in label:
            vertici = int(value)

    graph = Graph(vertici)

    for line in file:
        if "EOF" in line:
            break
        if "GEO" in type:
            tripla = list(map(float, line.split()))
        else:
            tripla = list(map(int, map(round, map(float, line.split()))))
        graph.add_node(int(tripla[0])-1, tripla[1], tripla[2])
    nodes = graph.get_nodes()
    for index_src in range(len(nodes)):
        for index_dest in range(index_src+1, len(nodes)):
            src = nodes[index_src]
            dest = nodes[index_dest]
            if "GEO" in type:
                graph.add_edge(src, dest, graph.geo_distance(src, dest))
            else:
                graph.add_edge(src, dest, graph.euclide_distance(src, dest))
    file.close()
    return graph


def errore(soluzione, ottimo):
    return str((soluzione-ottimo)/ottimo)


def main(folder, timeout):
    ottimi_file = open(folder+"/"+"ottimi.txt", "r")
    ottimi = {}
    for line in ottimi_file:
        graph, ottimo = list(line.split(":"))
        ottimi[graph] = int(ottimo)
    ottimi_file.close()
    with os.scandir(folder) as it:
        for i, entry in enumerate(it):
            if ".tsp" in entry.name:
                ottimo = ottimi[entry.name]
                graph = read_file(folder+"/"+entry.name)
                d_dist = {}
                p_dist = {}
                nodes = graph.get_nodes()
                global stop
                stop = False
                t = Timer(timeout, timeover)
                t.start()
                start = time.time()
                dist = held_karp(nodes[0], nodes[0], nodes, d_dist, p_dist)
                time_exec = time.time() - start
                t.cancel()
                test = entry.name.replace(".tsp", ".out")
                result = open(folder+"/"+test, "a")
                result.write("\nHeld Karp - soluzione: " +
                             str(dist)+" tempo: "+str(time_exec) + " errore: "+errore(dist, ottimo)+" %")
                result.close()


if __name__ == "__main__":
    sys.setrecursionlimit(999999999)
    main("tsp_dataset", int(sys.argv[1]))
