import math
import os
import random
import sys
from threading import Timer
import time


class Node():

    def __init__(self, name, index):
        self._name = name
        self._index = index
        self._adjacents = []
        self._visited = False

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

    def __hash__(self):
        return self._name

    def __ne__(self, other):
        return self._name != other._name

    def __repr__(self):
        return str(self._name)

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def adjacents(self):
        return self._adjacents

    def add_adjacent(self, node):
        self._adjacents.append(node)

    def set_adjacents(self, adjacents):
        self._adjacents = adjacents

    def visited(self):
        return self._visited

    def set_visited(self, visited):
        self._visited = visited

# %%


class Graph():

    def __init__(self, n):
        self._nodes = [None] * n
        self._lastnode = n

    def add_node(self, name, index):
        if not self.is_node_present(index):
            node = Node(name, index)
            self._nodes[index] = node
            return node
        else:
            return self._nodes[index]

    def nodes(self):
        return self._nodes

    def is_node_present(self, index):
        if self._nodes[index] is None:
            return False
        else:
            return True

    def num_vertici(self):
        return len(self._nodes)

    def inc_lastnode(self):
        self._lastnode += 1
        return self._lastnode


def karger(graph):
    nodes = graph.nodes()
    print(nodes)
    src_index = random.randint(0, len(nodes)-1)
    src = nodes[src_index]
    print(src)
    print(src.adjacents())
    for i in range(len(nodes)-2):
        adjacents_src = src.adjacents()
        dest = random.choice(adjacents_src)
        dest_index = dest.index()
        print(dest)
        print(dest.adjacents())
        adjacents_dest = dest.adjacents()
        newname = graph.inc_lastnode()
        adjacents_src = [adjacent for adjacent in adjacents_src if adjacent != dest]
        adjacents_dest = [adjacent for adjacent in adjacents_dest if adjacent != src]
        newadjacents = adjacents_src + adjacents_dest
        newnode = Node(newname, dest.index())
        newnode.set_adjacents(newadjacents)
        print(newnode)
        print(newadjacents)
        for node in newadjacents:
            adjacents = node.adjacents()
            for i, adjacent in enumerate(adjacents):
                if adjacent is src or adjacent is dest:
                    adjacents[i] = newnode
        nodes[src_index] = None
        nodes[dest_index] = newnode
        src = newnode
        src_index = src.index()


def read_file(filename):
    file = open(filename, "r")
    graph = Graph(len(file.readlines()))
    file.seek(0)
    for line in file:
        nodi = line.split()
        for i, name in enumerate(nodi):
            intname = int(name)
            if i is 0:
                root = graph.add_node(intname, intname-1)
            else:
                node = graph.add_node(intname, intname-1)
                root.add_adjacent(node)
    file.close()
    return graph


def errore(soluzione, ottimo):
    return str((soluzione-ottimo)/ottimo)


def main(folder):
    with os.scandir(folder) as it:
        for i, entry in enumerate(it):
            if "input_random_1_6" in entry.name:
                graph = read_file(folder+"/"+entry.name)
                karger(graph)
                nodes = graph.nodes()
                for node in nodes:
                    if node is not None:
                        print(node)
                        for adjacent in node.adjacents():
                            if adjacent is not None:
                                print("  "+str(adjacent))
                """print(entry.name)
                start = time.time()
                dist = cheapest_insertion(graph)
                time_exec = time.time() - start
                test = entry.name.replace(".tsp", ".out")
                result = open(folder+"/"+test, "a")
                result.write("\nCheapest_Insertion - soluzione: " +
                             str(dist)+" tempo: "+str(time_exec) + " errore: "+errore(dist, ottimo)+" %")
                result.close()"""


if __name__ == "__main__":
    main("mincut_dataset")
