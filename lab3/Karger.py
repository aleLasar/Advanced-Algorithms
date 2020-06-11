import argparse
import copy
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


def full_contraction(graph):
    nodes = graph.nodes()
    not_removed = list(nodes)
    for i in range(len(nodes)-2):
        src_index = random.randint(0, len(not_removed)-1)
        src = not_removed[src_index]
        adjacents_src = src.adjacents()
        dest = random.choice(adjacents_src)
        dest_index = dest.index()
        adjacents_dest = dest.adjacents()
        newname = graph.inc_lastnode()
        adjacents_src = [
            adjacent for adjacent in adjacents_src if adjacent != dest
        ]
        adjacents_dest = [
            adjacent for adjacent in adjacents_dest if adjacent != src
        ]
        newadjacents = adjacents_src + adjacents_dest
        newnode = Node(newname, dest_index)
        newnode.set_adjacents(newadjacents)
        for node in newadjacents:
            adjacents = node.adjacents()
            for i, adjacent in enumerate(adjacents):
                if adjacent is src or adjacent is dest:
                    adjacents[i] = newnode
        nodes[src_index] = None
        nodes[dest_index] = newnode
        del not_removed[src_index]

    mincut = 0
    for node in not_removed:
        if node is not None:
            for adjacent in node.adjacents():
                if adjacent is not None:
                    mincut += 1
            break
    return mincut


def karger(graph, k, ottimo):
    mincut = float("inf")
    original = copy.deepcopy(graph)
    time_fc = 0
    time_discovery = 0
    for _ in range(k):
        fc_start = time.time()
        fc = full_contraction(graph)
        if fc == ottimo:
            time_discovery = time.time() - fc_start
        elif fc < ottimo:
            ottimo = fc
            time_discovery = time.time() - fc_start
        time_fc += time.time() - fc_start
        if fc < mincut:
            mincut = fc
        graph = copy.deepcopy(original)
    time_fc = int(time_fc / k)
    return mincut, time_fc, time_discovery


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
    return (soluzione-ottimo)/ottimo


def main(folder, d=1):
    with os.scandir(folder) as it:
        for entry in it:
            graph = read_file(folder+"/"+entry.name)
            n = len(graph.nodes())
            k = math.ceil(d * math.pow(n, 2) / 2 * math.log(n))
            file = open(folder + '/' +
                        entry.name.replace("input", "output"), "r")
            ottimo = int(file.readline())
            file.close()
            karger_start = time.time()
            mincut, time_fc, time_discovery = karger(graph, k, ottimo)
            time_karger = time.time() - karger_start
            if mincut < ottimo:
                ottimo = mincut
                file = open(folder + '/' +
                            entry.name.replace("input", "output_nostro"), "w")
                file.write(mincut)
                file.close()
            errore_perc = errore(mincut, ottimo)*100
            file = open(folder + '/' +
                        entry.name.replace("input", "risultati"), "w")
            file.write("time_fc:"+str(time_fc)+" time_discovery:"+str(time_discovery) +
                       " time_karger:"+str(time_karger)+" errore_perc:"+str(errore_perc))
            file.close()


if __name__ == "__main__":
    sys.setrecursionlimit(999999999)
    parser = argparse.ArgumentParser(description='Laboratorio 3 - Minimum Cut')
    parser.add_argument('d', default=1, type=int, nargs='?',
                        help='Parametro per identificare la probabilità che l\'algoritmo abbia successo come esponente del denominatore (default =1).')
    args = parser.parse_args()
    main("mincut_dataset", int(args.d))
