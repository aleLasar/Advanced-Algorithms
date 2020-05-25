# %%

import math
import os
import sys
import time

PI = 3.141592
RRR = 6378.388


class Heap():

    def __init__(self):
        self._list = []
        self._ultimo = -1

    def push(self, value):
        self._ultimo += 1
        self._list.append(value)
        value._position = self._ultimo
        self._orderup(self._ultimo)

    def pop(self):
        if self._ultimo == -1:
            raise IndexError('Heap vuoto')

        min_value = self._list[0]
        self._list[0], self._list[self._ultimo] = self._list[self._ultimo], self._list[0]
        self._list[0]._position, self._list[self._ultimo]._position =\
            self._list[self._ultimo]._position, self._list[0]._position
        self._ultimo -= 1
        self._orderdown(0)
        min_value.set_present(False)
        return min_value

    def _orderup(self, index):
        while index > 0:
            p_index, p_value = self._get_parent(index)
            if p_value <= self._list[index]:
                break
            self._list[p_index], self._list[index] = self._list[index], self._list[p_index]
            self._list[p_index]._position, self._list[index]._position =\
                self._list[index]._position, self._list[p_index]._position
            index = p_index

    def _orderdown(self, index):
        while index <= self._ultimo:
            value = self._list[index]
            left_child_index, left_child_value = self._get_left_child(index)
            right_child_index, right_child_value = self._get_right_child(index)
            if left_child_index <= self._ultimo and right_child_index <= self._ultimo:
                if value <= left_child_value and value <= right_child_value:
                    break
                if left_child_value < right_child_value:
                    new_index = left_child_index
                else:
                    new_index = right_child_index
            elif left_child_index <= self._ultimo and left_child_value <= value:
                new_index = left_child_index
            elif right_child_index <= self._ultimo and right_child_value <= value:
                new_index = right_child_index
            else:
                break
            self._list[new_index], self._list[index] = self._list[index], self._list[new_index]
            self._list[new_index]._position, self._list[index]._position =\
                self._list[index]._position, self._list[new_index]._position
            index = new_index

    def _get_parent(self, index: int):
        if index == 0:
            return -1, False
        p_index = (index - 1) // 2
        return p_index, self._list[p_index]

    def _get_left_child(self, index: int):
        left_child_index = 2 * index + 1
        if left_child_index > self._ultimo:
            return left_child_index, False
        return left_child_index, self._list[left_child_index]

    def _get_right_child(self, index: int):
        right_child_index = 2 * index + 2
        if right_child_index > self._ultimo:
            return right_child_index, False
        return right_child_index, self._list[right_child_index]

    def __len__(self):
        return self._ultimo + 1

    def __str__(self):
        result = "["
        for element in self._list:
            result += str(element.key()) + ","
        result += "]"
        return result

# %%


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
        deg = math.trunc(self._latitude)
        rounded = self._latitude - deg
        return PI * (deg + 5.0 * (rounded / 3.0)) / 180.0

    def set_latitude(self, latitude):
        self._latitude = latitude

    def longitude(self):
        return self._longitude

    def longitude_rad(self):
        deg = math.trunc(self._longitude)
        rounded = self._longitude - deg
        return PI * (deg + 5.0 * (rounded / 3.0)) / 180.0

    def set_longitude(self, longitude):
        self._longitude = longitude

    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)


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

# %%


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
        return math.trunc(RRR * math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)

    def euclide_distance(self, src, dest):
        x = src.latitude() - dest.latitude()
        y = src.longitude() - dest.longitude()
        return round(math.trunc(math.sqrt(math.pow(x, 2)+math.pow(y, 2))))

# %%


def prim(graph, s):
    #mst_weight = 0
    adjacency_list = graph.get_graph()
    adjacency_list[s].set_key(0)
    heap_keys = Heap()
    for node in adjacency_list:
        heap_keys.push(node)
    while len(heap_keys) != 0:
        u = heap_keys.pop()
        adjacents = adjacency_list[u.name()].edges()
        for edge in adjacents:
            v = edge.node()
            if(v.present() and edge.weight() < v.key()):
                v.set_parent(u)
                v.set_key(edge.weight())
                heap_keys._orderup(v._position)
        #mst_weight += u.key()
    for node in adjacency_list:
        if node.parent():
            parent = node.parent()
            parent.add_child(node)
    # return graph


def preorder(preordered, v):
    preordered.append(v)
    for child in v.children():
        preorder(preordered, child)


def approx_t_tsp(graph, s):
    prim(graph, s)
    nodes = graph.get_graph()
    preordered = []
    preorder(preordered, nodes[s])
    preordered.append(nodes[s])
    return preordered


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

def errore(soluzione, ottimo):
    return str((soluzione-ottimo)/ottimo)

def main(folder):
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
                start = time.time()
                preordered = approx_t_tsp(graph, 0)
                weight = 0
                for node in preordered:
                    weight += 2 * node.key()
                time_exec = time.time() - start
                test = entry.name.replace(".tsp", ".out")
                result = open(folder+"/"+test, "a")
                result.write("\n2attsp - soluzione: " +
                             str(weight)+" tempo: "+str(time_exec) + " errore: "+errore(weight, ottimo)+" %")
                result.close()


if __name__ == "__main__":
    sys.setrecursionlimit(999999999)
    main("tsp_dataset")

# %%
