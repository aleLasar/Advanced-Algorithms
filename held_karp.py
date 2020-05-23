import math
import os
import sys
import time

PI = 3.141592
RRR = 6378.388


class Node():

    def __init__(self, name, latitude, longitude):
        self._name = name
        self._key = sys.maxsize
        self._parent = None
        self._position = None
        self._present = True
        self._edges = []
        self._latitude = latitude
        self._longitude = longitude
        self._children = []

    def __gt__(self, other):
        return self._key > other._key

    def __lt__(self, other):
        return self._key < other._key

    def __le__(self, other):
        return self._key <= other._key

    def __ge__(self, other):
        return self._key >= other._key

    def __eq__(self, other):
        return self._key == other._key

    def __ne__(self, other):
        return self._key != other._key

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def key(self):
        return self._key

    def set_key(self, key):
        self._key = key

    def parent(self):
        return self._parent

    def set_parent(self, parent):
        self._parent = parent

    def edges(self):
        return self._edges

    def add_edge(self, edge):
        self._edges.append(edge)

    def position(self):
        return self._position

    def present(self):
        return self._present

    def set_present(self, present):
        self._present = present

    def latitude(self):
        return self._latitude

    def latitude_rad(self):
        deg = int(self._latitude)
        rounded = self._latitude - deg
        return PI * (deg + 5.0 * rounded / 3.0) / 180.0

    def set_latitude(self, latitude):
        self._latitude = latitude

    def longitude(self):
        return self._longitude

    def longitude_rad(self):
        deg = int(self._longitude)
        rounded = self._longitude - deg
        return PI * (deg + 5.0 * rounded / 3.0) / 180.0

    def set_longitude(self, longitude):
        self._longitude = longitude

    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

    #dest = Node
    def find_edge(self, dest):
        for x in self._edges:
            if x.node() == dest:
                return x
        return None        


class Edge():

    def __init__(self, node, weight):
        self._node = node
        self._weight = weight

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

    def weight(self):
        return self._weight

    def node(self):
        return self._node


class Graph():

    def __init__(self, n):
        self._nodes = [None] * n

    def add_node(self, name, latitude, longitude):
        if not self.is_node_present(name):
            node = Node(name, latitude, longitude)
            self._nodes[name] = node
            return node
        else:
            return self._nodes[name]

    def add_edge(self, src, dest, weight):
        edge = Edge(dest, weight)
        self._nodes[src.name()].add_edge(edge)
        edge2 = Edge(src, weight)
        self._nodes[dest.name()].add_edge(edge2)

    def get_graph(self):
        return self._nodes

    def is_node_present(self, name):
        return self._nodes[name] is not None

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
start =  nodo di partenza
v = nodo
S = lista di vertici
d_dict = dizionario: indici [n, str(S)]
p_dict = dizionario: indici [n, str(S)]
"""


def held_karp(start, v, S: list, d_dict, p_dict):
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
            dist = held_karp(start, S[i], S2, d_dict, p_dict)
            uv_weight = S[i].find_edge(v).weight()
            if(dist + uv_weight < mindist):
                mindist = dist + uv_weight
                minprec = S[i]
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
    nodes = graph.get_graph()
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


def main(folder):
    with os.scandir(folder) as it:
        for i, entry in enumerate(it):
            if "ulysses16" in entry.name:
                graph = read_file(folder+"/"+entry.name)
                d_dist = {}
                p_dist = {}
                nodes = graph.get_graph()
                dist = held_karp(nodes[0], nodes[0], nodes, d_dist, p_dist)
                print(str(dist))          


if __name__ == "__main__":
    main("tsp_dataset")
