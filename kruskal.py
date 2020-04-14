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
class Node():
    
    def __init__(self,name):
        self._name = name
        self._visited = False
        self._edges = []

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

    def name(self):
        return self._name

    def set_name(self,name):
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
class UnionFind():

    def __init__(self, n):
        self._parents = [None] * n
        for i in range(0, n):
            self._parents[i] = i        

    def find(self, x, depth=0):
        if (x != self._parents[x]):
            return self.find(self._parents[x], depth+1)
        return x, depth

    def union(self, x, y):
        set_x, depth_x = self.find(x)
        set_y, depth_y = self.find(y)
        if(set_x == set_y):
            return
        if(depth_x > depth_y):
            self._parents[set_y] = set_x
        else:
            self._parents[set_x] = set_y

# %%
class Graph():

    def __init__(self, n):
        self._nodes = [None] * n
        self._edges = []

    def add_node(self, name):
        if not self.is_node_present(name):
            node = Node(name)
            self._nodes[name] = node
            return node
        else:
            return self._nodes[name]

    def add_edge(self, src, dest, weight):
        edge = Edge(src, dest, weight)
        self._edges.append(edge)
        self._nodes[src.name()].add_edge(edge)
        edge2 = Edge(dest, src, weight)
        self._nodes[dest.name()].add_edge(edge2)

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
        
    def _merge(self, left, middle, right): 
        dim_left = middle - left + 1
        dim_right = right - middle 
        left_array = [0] * dim_left 
        right_array = [0] * dim_right
        
        for i in range(0 , dim_left): 
            left_array[i] = self._edges[left + i] 
    
        for j in range(0 , dim_right): 
            right_array[j] = self._edges[middle + 1 + j] 
    
        i = 0
        j = 0 
        k = left
    
        while i < dim_left and j < dim_right : 
            if left_array[i] <= right_array[j]: 
                self._edges[k] = left_array[i] 
                i += 1
            else: 
                self._edges[k] = right_array[j] 
                j += 1
            k += 1
         
        while i < dim_left: 
            self._edges[k] = left_array[i] 
            i += 1
            k += 1
        
        while j < dim_right: 
            self._edges[k] = right_array[j] 
            j += 1
            k += 1

    def _mergeSort(self, left, right): 
        if left < right: 
            middle = (left + (right-1)) // 2    
            self._mergeSort(left, middle) 
            self._mergeSort(middle + 1, right) 
            self._merge(left, middle, right) 

    def ordinaLati(self):
        self._mergeSort(0, len(self._edges)-1)          


# %% [markdown]
# # Algoritmo di Kruskal
# 
# ## Kruskal
# 
# ```
# Kruskal(G)
#   
#   A = {}
# 
#   U = initialize(V)
#   sort edges of E by cost
#   for each edge = (v,w) in non decreasing order of cost do:
#       if find(U,v) != find(U,w):
#           A = A U {(v,w)}
#           Union(U,v,w)
#   return A
#
# ```

# %%
import os
import sys

def kruskal(graph, s):
    mst_weight = 0
    mst = Graph(graph.num_vertici())
    union_find = UnionFind(graph.num_vertici())
    graph.ordinaLati()
    for edge in graph.get_edges():
        x = union_find.find(edge.nodes()[0].name())
        y = union_find.find(edge.nodes()[1].name())
        if x[0] != y[0]:
            s1 = mst.add_node(edge.nodes()[0].name())
            d1 = mst.add_node(edge.nodes()[1].name())
            mst.add_edge(s1, d1, edge._weight)
            union_find.union(s1.name(), d1.name())
            mst_weight += edge.weight()    
    return mst_weight

def read_file(filename):
    file = open(filename, "r")
    vertici, archi = list(map(int, file.readline().split()))
    graph = Graph(vertici)
    for line in file:
        tripla = list(map(int, line.split()))
        src = graph.add_node(tripla[0]-1)
        dest = graph.add_node(tripla[1]-1)
        graph.add_edge(src, dest, tripla[2])
    file.close()
    return graph

def main(folder):
    with os.scandir(folder) as it:
        for i,entry in enumerate(it):
            if "input_random" in entry.name:
                graph = read_file(folder+"/"+entry.name)
                weight = kruskal(graph, 0)
                test = entry.name.replace("input_random","output_random")
                with open(folder+"/"+test) as f:
                    result = int(f.read().split()[0])
                    if weight != result:
                        print("Our result: "+str(weight))
                        print("Correct: "+str(result))
                        print("Graph: "+str(entry.name))
                        break

if __name__ == "__main__":
    main("mst-dataset")


# %%
