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

    def __gt__(self, other): 
        if(self._name > other._name): 
            return True
        else: 
            return False

    def __lt__(self, other): 
        if(self._name < other._name): 
            return True
        else: 
            return False

    def __le__(self, other): 
        if(self._name <= other._name): 
            return True
        else: 
            return False

    def __ge__(self, other): 
        if(self._name >= other._name): 
            return True
        else: 
            return False

    def __eq__(self, other): 
        if(self._name == other._name): 
            return True
        else: 
            return False

    def __ne__(self, other): 
        if(self._name != other._name): 
            return True
        else: 
            return False

    def name(self):
        return self._name

    def set_name(self,name):
        self._name = name
            
class Edge():

    def __init__(self, src, dest, weight):
        self._nodes = src, dest
        self._weight = weight

    def __gt__(self, other): 
        if(self._weight > other._weight): 
            return True
        else: 
            return False

    def __lt__(self, other): 
        if(self._weight < other._weight): 
            return True
        else: 
            return False

    def __le__(self, other): 
        if(self._weight <= other._weight): 
            return True
        else: 
            return False

    def __ge__(self, other): 
        if(self._weight >= other._weight): 
            return True
        else: 
            return False

    def __eq__(self, other): 
        if(self._weight == other._weight): 
            return True
        else: 
            return False

    def __ne__(self, other): 
        if(self._weight != other._weight): 
            return True
        else: 
            return False

    def weight(self):
        return self._weight

    def nodes(self):
        return self._nodes


# %%
class Graph():

    def __init__(self,n):
        self._edges = [None] * n

    def add_node(self, name):
        pass

    def add_edge(self, src, dest, weight):
        pass

    def get_graph(self):
        return self._edges

    

# %% [markdown]
# # Algoritmo di Kruskal
# 
# ## Kruskal naive
# 
# ```
# Kruskal(G)
#   
#   A = {}
# 
#   sort edges of G by cost (mergesort)
#   for each edge e in nondecreasing order of cost do:
#     if A U {e} is acyclic then:
#       A = A U {e}
#   return A
# ```

# %%
import os
import sys

def kruskal(graph, s):
    pass  

def read_file(filename):
    pass

if __name__ == "__main__":
    pass


# %%
