# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Minimum Spanning Trees
# 
# ## Algoritmi
# 
# Gli algoritmi da implementare sono tre:
# 
# - **Algoritmo di Prim** implementato con Heap
# - **Algoritmo di Kruskal** nella sua implementazione "naive" di complessità O(mn)
# - **Algoritmo di Kruskal** implementato con Union-Find
# 
# ## Dataset
# 
# Il dataset contiene 68 grafi di esempio, di dimensione compresa tra 10 e 100000 vertici, generati in modo randomico con il TestCaseGenerator di [stanford-algs](https://github.com/beaunus/stanford-algs/tree/master/testCases/course3/assignment1SchedulingAndMST/question3). Ogni file descrive un grafo non orientato con pesi interi usando il seguente formato:
# 
# ```
# [numero_di_vertici] [numero_di_archi] 
# [un_vertice_arco_1] [altro_vertice_arco_1] [peso_arco_1] 
# [un_vertice_arco_2] [altro_vertice_arco_2] [peso_arco_2] 
# [un_vertice_arco_3] [altro_vertice_arco_3] [peso_arco_3] 
# ...
# ```
# 
# Ad esempio, una riga "2 3 -8874" indica che esiste un arco che collega il vertice 2 al vertice 3 con peso -8874. NON si deve presumere che i pesi siano positivi, né che siano distinti.
# 
# ## Domanda 1
# 
# Eseguite i tre algoritmi che avete implementato (Prim, Kruskal naive e Kruskal efficiente) sui grafi del dataset. Misurate i tempi di calcolo dei tre algoritmi e create un grafico che mostri la variazione dei tempi di calcolo al variare del numero di vertici nel grafo. Per ognuna delle istanze del problema, riportate il peso del minimum spanning tree ottenuto dagli algoritmi. 
# 
# ## Domanda 2
# 
# Commentate i risultati che avete ottenuto: come si comportano gli algoritmi rispetti alle varie istanze? C'è un algoritmo che riesce sempre a fare meglio degli altri? Quale dei tre algoritmi che avete implementato è più efficiente?
# 
# ## Cosa consegnare
# 
# - Una breve relazione sullo svolgimento del progetto. La relazione deve contenere:
#   - una sezione introduttiva con la descrizione degli algoritmi e delle scelte implementative che avete fatto;
#   - grafici esplicativi dei risultati con le risposte alle due domande;
#   - eventuali originalità introdotte nell'elaborato o nell'implementazione;
#   - una sezione conclusiva in cui porre i vostri commenti e le vostre conclusioni sull’elaborato svolto e i risultati ottenuti.
# - Il codice sorgente dell’implementazione in un unico file di archivio (.zip, .tar.gz, ecc.).
# 
# ## Note generali
# - L'esercitazione si può implementare con qualsiasi linguaggio di programmazione. Strutture dati di base come liste, code, pile, insiemi, dizionari o mappe, messe a disposizione dalle librerie standard del linguaggio, sono utilizzabili senza restrizioni. Non è consentito utilizzare librerie che forniscono direttamente le strutture dati e gli algoritmi per rappresentare e manipolare grafi, come NetworkX, JGraphT o simili.
# - Commenta le parti essenziali del codice in modo che sia possibile cogliere le idee che hanno portato alla scrittura di quel codice. I commenti aiuteranno a chiarire se un bug è un errore concettuale o solo un piccolo errore.
# - Il laboratorio può essere svolto sia da soli che in gruppi di massimo tre persone.
# - Solo uno dei componenti del gruppo consegna l'elaborato, indicando i nomi dei componenti del gruppo nella relazione e nello spazio sottostante.
# - La prima esercitazione va consegnata entro le **ore 23:55 di lunedì 4 maggio.** Consegne in ritardo comportano una penalizzazione sul voto.

# %%
class Heap():

    def __init__(self):
        self._list = []
        self._ultimo = -1

    def push(self, value):
        self._ultimo += 1
        self._list.append(value)
        self._orderup(self._ultimo)

    def pop(self):
        if self._ultimo == -1:
            raise IndexError('Heap vuoto')

        min_value = self._list[0]

        self._list[0] = self._list[self._ultimo]
        self._ultimo -= 1
        self._orderdown(0)

        return min_value

    def is_present(self, search):
        if self._ultimo == -1:
            raise IndexError('Heap vuoto')
        index, value = 0, self._list[0]
        while(index < last and index != None):
            if(search == value):
                return True
            if(search < value):
                index, value = _get_right_child(index)
            else:
                index, value = _get_left_child(index)
        return False

    def _orderup(self, index: int):
        if index > 0:
            p_index, p_value = self._get_parent(index)
            if p_value <= self._list[index]:
                return
            self._list[p_index], self._list[index] = self._list[index], self._list[p_index]
            index = p_index
            self._orderup(index)

    def _orderdown(self, index: int):
        while True:
            index_value = self._list[index]
            left_child_index, left_child_value = self._get_left_child(index)
            right_child_index, right_child_value = self._get_right_child(index)
            if index_value <= left_child_value and index_value <= right_child_value:
                break
            if left_child_value < right_child_value:
                new_index = left_child_index
            else:
                new_index = right_child_index
            self._list[new_index], self._list[index] = self._list[index], self._list[new_index]
            index = new_index

    def _get_parent(self, index: int):
        if index == 0:
            return None, None
        p_index = (index - 1) // 2
        return p_index, self._list[p_index]

    def _get_left_child(self, index: int):
        left_child_index = 2 * index + 1
        if left_child_index > self._ultimo:
            node = Node(None)
            node.set_key(sys.maxsize)
            return None, node

        return left_child_index, self._list[left_child_index]

    def _get_right_child(self, index: int):
        right_child_index = 2 * index + 2
        if right_child_index > self._ultimo:
            node = Node(None)
            node.set_key(sys.maxsize)
            return None, node
        return right_child_index, self._list[right_child_index]

    def __len__(self):
        return self._ultimo+1


# %%
class UnionFind():

    def __init__(self):
        self._parents = []
    
    def initialize(self, n: int):
        for i in range(0,n):
            self._parents[i] = i

    def find(self, x, depth=0):
        if (x != self._parents[x]):
            return self.find(self._parents[x], depth+1)
        return x, depth

    def union(self, x, y):
        set_x, depth_x = find(x)
        set_y, depth_y = find(y)
        if(set_x == set_y):
            return
        if(depth_x > depth_y):
            self._parents[set_y] = set_x
        else:
            self._parents[set_x] = set_y


# %%
class Node():
    
    def __init__(self,name):
        self._name = name
        self._key = sys.maxsize
        self._parent = None
        self._edges = []

    def __gt__(self, other): 
        if(self._key > other._key): 
            return True
        else: 
            return False

    def __lt__(self, other): 
        if(self._key < other._key): 
            return True
        else: 
            return False

    def __le__(self, other): 
        if(self._key <= other._key): 
            return True
        else: 
            return False

    def __ge__(self, other): 
        if(self._key >= other._key): 
            return True
        else: 
            return False

    def __eq__(self, other): 
        if(self._key == other._key): 
            return True
        else: 
            return False

    def __ne__(self, other): 
        if(self._key != other._key): 
            return True
        else: 
            return False

    def name(self):
        return self._name

    def set_name(self,name):
        self._name = name

    def key(self):
        return self._key

    def set_key(self,key):
        self._key = key

    def parent(self):
        return self._parent

    def set_parent(self, parent):
        self._parent = parent

    def edges(self):
        return self._edges
    
    def add_edge(self, edge):
        self._edges.append(edge)

    def label(self):
        return self._label
    
    def set_label(self, label):
        self._label = label

class Edge():

    def __init__(self, src, dest, weight):
        self._src = src
        self._dest = dest
        self._weight = weight
        self._label=""

    def __gt__(self, other): 
        if(self._key > other._weight): 
            return True
        else: 
            return False

    def __lt__(self, other): 
        if(self._key < other._weight): 
            return True
        else: 
            return False

    def __le__(self, other): 
        if(self._key <= other._weight): 
            return True
        else: 
            return False

    def __ge__(self, other): 
        if(self._key >= other._weight): 
            return True
        else: 
            return False

    def __eq__(self, other): 
        if(self._key == other._weight): 
            return True
        else: 
            return False

    def __ne__(self, other): 
        if(self._key != other._weight): 
            return True
        else: 
            return False

    def weight(self):
        return self._weight

    def nodes(self):
        return self._src, self._dest

    def opposite(self,node):
        if self._src == node:
            return self._dest
        return self._src


# %%
class Graph():

    def __init__(self):
        self._nodes = []

    def add_node(self, node):
        if not self.is_node_present(node):
            self._nodes.append(node)

    def add_edge(self, src, dest, weight):
        edge = Edge(src,dest,weight)
        self._nodes[src.name()].add_edge(edge)
        self._nodes[dest.name()].add_edge(edge)

    def get_graph(self):
        """for (i,node) in enumerate(self._nodes):
            print("Node: "+str(node.name()+1))
            for edge in node.edges():
                print("Dest: "+str(edge.node().name()+1)+" Weight: "+str(edge.weight())+" | ")"""
        return self._nodes

    def is_node_present(self,node):
        if node.name() in map(lambda x: x.name(), self._nodes):
            return True
        return False

    #implemented with mergeSort
    #def order_inc_nodes(self):
             

    def isCyclic(self): 
        visited =[False]*(len(self._nodes)) 
        for i in range(len(self._nodes)): 
            if visited[i] ==False:
                if(self._isCyclicUtil(i,visited,-1))== True: 
                    return True
          
        return False
    
    def _isCyclicUtil(self,v:int,visited,parent): 
        visited[v]= True
        vicini = self._nodes[v]._edges
        for i in vicini: 
            if i._dest._name != v:
                # If the node is not visited then recurse on it 
                if  visited[i._dest._name]==False :  
                    if(self._isCyclicUtil(i._dest._name,visited,v)): 
                        return True
                # If an adjacent vertex is visited and not parent of current vertex, 
                # then there is a cycle 
                elif  parent!=i._dest._name: 
                    return True
          
        return False

# %% [markdown]
# # Algoritmo di Prim
# 
# ## Prim di base
# 
# ```
# Prim(G,s)
#   
#   X = {s}
#   A = empty;
# 
#   while edge in (u,v), u in X, v not in X:
#     (u*, v*) = light edge
#     add v* to X
#     add (u*, v*) to A
# 
#   return A
# ```
# 
# ## Prim con heap
# 
# ```
# Prim(G,s)
#   foreach u in V:
#     key[u] = infinity
#     parent[u] = null
#   key[s] = 0
#   Q = V
#   while Q not empty:
#     u = extractMin(Q)
#     foreach v adjacent_to u:
#       if v in Q and w(u,v) < key[v]:
#         parent[v] = u
#         key[v] = w(u,v)
#   return V\Q
# ```

# %%
#import os
import sys

def prim(graph, s):
    adjacency_list = graph.get_graph()
    adjacency_list[s].set_key(0)
    heap = Heap()
    mst = Heap()
    for node in adjacency_list:
        heap.push(node)
    while len(heap) !=0:
        u = heap.pop()
        adjacents = adjacency_list[u.name()].edges()
        print("Node: "+str(u.name())+" "+str(u)+" key "+str(u.key()))
        for edge in adjacents:
            v = edge.opposite(u)
            print("Dest: "+str(v.name())+" "+str(v) +" key "+str(v.key()))
            if(edge.weight() < v.key()):
                print("New edge chosen")
                v.set_parent(u)
                v.set_key(edge.weight())
                print("key "+str(v.key()))
        mst.push(u)
    while(len(mst)!=0):
        u = mst.pop()
        print("Node: "+str(u.name()+1))
        if(u.parent()):
            print("Parent: "+str(u.parent().name()+1))
        else:
            print("Parent: None")
        print("Key: "+str(u.key()))

def kruskal_1(graph: Graph):
    forest= Graph()
    #graph.order_inc_nodes()
    

def read_file(filename):
    file = open(filename, "r")
    vertici, archi = list(map(int, file.readline().split()))
    graph = Graph()
    for line in file:
        tripla = list(map(int, line.split()))
        if tripla[0] != tripla[1]:
            src = Node(tripla[0]-1)
            dest = Node(tripla[1]-1)
            graph.add_node(src)
            graph.add_node(dest)
            graph.add_edge(src, dest, tripla[2])
    file.close()
    return graph

if __name__ == "__main__":
    """with os.scandir('mst-dataset') as it:
        for i,entry in enumerate(it):
            if i == 0:
                continue
            if not entry.name.startswith('.') and entry.is_file():
                graph = read_file('mst-dataset/'+entry.name)
                prim(graph, 0)
                if i == 1:
                    break
    """
    graph = read_file('mst-dataset/input_random_01_10.txt')
    p=graph.isCyclic()
    print(p)


# %%


