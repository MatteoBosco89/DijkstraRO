import sys
import random


# classe VERTEX
# rappresenta il nodo del grafo

class Vertex:

    def __init__(self, node):
        # identificativo nodo
        self.id = node 
        # dizionario dei nodi adiacenti, salvati come nodo - distanza dal nodo
        self.adjacent = {} 
        # la distanza iniziale viene settata a infinito
        # usato per Dijkstra
        self.distance = sys.maxsize 
        # setta se il nodo è stato visitato o no
        # usato per Dijkstra
        self.visited = False  
        # setta il predecessore a None
        # usato per Dijkstra
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def not_visited(self):
        self.visited = False

    def __str__(self):
        return str(self.id)

    def __lt__(self, other):
        if(self.get_distance() < other.get_distance()):
            return self
    
    # il peso può essere randomico se richiesto
    def gen_random_weight(self): 
        for k in self.adjacent.keys():
            self.adjacent[k] = random.randint(0, 30)


# classe Grafo

class Graph:

    def __init__(self):
        self.vert_dict = {} # dizionario dei nodi
        self.num_vertices = 0 # numero di nodi nel grafo

    def __iter__(self):
        return iter(self.vert_dict.values())
    
    # creazione ed aggiunta NODO
    def add_vertex(self, node): 
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    # creazione ed aggiunta ARCO
    # controlla se i nodi esistono
    def add_edge(self, frm, to, cost=0): 
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)

    def reset_distance(self):
        for v in self:
            v.set_distance(sys.maxsize)

    def reset_visited(self):
        for v in self:
            v.not_visited()

    def gen_random_weight(self):
        for v in self:
            v.gen_random_weight()

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous
    
    # stampa il grafo come coppia di nodi con il peso dell'arco
    def print_graph_data(self):
        print('Graph data:')
        for v in self:
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))
    
    # ricostruisce il path minimo a partire dai
    # predecessori ricavati dall'algoritmo di Dijkstra (ricorsivo)
    def shortest(self, v, path):
        if v.previous:
            path.append(v.previous.get_id())
            self.shortest(v.previous, path)
        return

    # ALGORITMO DIJKSTRA
    def dijkstra(self, start, target):
        start.set_previous(None)
        start.set_distance(0)
        # creazione di un heap
        # per conservare i nodi da visitare
        unvisited_heap = []
        for v in self:
            unvisited_heap.append((v.get_distance(), v))
        unvisited_heap.sort()
    
        # l'algoritmo prende l'elemento in testa all'heap 
        # e va a vedere i nodi che può visitare
        while len(unvisited_heap):
            uv = unvisited_heap.pop(0)
            curr = uv[1]
            curr.set_visited()
            # se il nodo visitato è quello
            # che si vuole raggiungere termina l'algoritmo
            if(curr is target): 
                break
            # esplorazione dei nodi adiacenti
            # aggiornamento delle distanze provvisorie 
            # e dei predecessori
            for next in curr.adjacent:
                if not next.visited:
                    distance = curr.get_distance() + curr.get_weight(next)
                    if(distance < next.get_distance()):
                        next.set_distance(distance)
                        next.set_previous(curr)
                        # print('updated : current = ' + str(curr.get_id()) + ' next = ' + str(next.get_id()) + ' new_dist = ' + str(next.get_distance()))
            # ricostruisce l'heap sulla base delle nuove distanze trovate
            unvisited_heap = []
            for v in self:
                if not v.visited:
                    unvisited_heap.append((v.get_distance(), v))
            unvisited_heap.sort()
        path = [target.get_id()]
        self.shortest(target, path) # ricostruzione del path a costo minimo e stampa
        print('The shortest path : %s' % (path[::-1]))
        print('The weight of the shortest path is: ' + str(target.get_distance()))

        return path

# MAIN

if __name__ == '__main__':
    
    # creazione e costruzione grafo
    g = Graph() 

    for i in range(1, 37):
        g.add_vertex(i)

    file = open("Map.txt")
    for line in file:
        arc = line.split(",")
        n1 = int(arc[0])
        n2 = int(arc[1])
        n3 = int(arc[2])
        g.add_edge(n1, n2, n3)

    g.print_graph_data()
    
    # richiesta del nodo di partenza e di arrivo
    # in base al grafo datogli in pasto da file
    while True:

        start = int(input("Insert start node: "))
        target = int(input("Insert target node: "))

        # esecuzione algoritmo
        g.dijkstra(g.get_vertex(start), g.get_vertex(target)) 
        
        # reset etichettamento
        g.reset_distance()
        g.reset_visited()

        # piccolo menù
        print("\nDo you want to continue?")
        print("Insert n to stop")
        print("Insert u to continue and update weight on graph")
        print("Insert any character to continue without update the weight")
        cmd = input(">>")
        if "n" in cmd:
            break
        elif "u" in cmd:
            g.gen_random_weight()
        g.print_graph_data()
