from Dijkstra import Graph
import random
import sys


#   Classe BUS per identificare le navette

class Bus:
    position = 0  # posizione del BUS (id del nodo)
    standing_point = 0 # standing-point assegnato al BUS
    id = 0  # id del BUS
    destination = 0  # id nodo destinazione
    MAXSEAT = 10    # numero posti massimo
    currSeat = 0    # posti occupati

    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_standing_point(self, value):
        self.standing_point = value

    def get_standing_point(self):
        return self.standing_point

    def get_position(self):
        return self.position

    def get_destination(self):
        return self.destination

    def updatePosition(self, position):
        self.position = position

    def updateDestination(self, destination):
        self.destination = destination

    def get_passengers(self):
        return self.currSeat
    
    # quando aggiunge i passeggeri controlla se ha raggiunto il massimo
    # se il numero massimo viene raggiunto, ritorna il numero
    # di persone rimaste alla fermata (leftover)
    
    def loadPassengers(self, passengers): 
        if(passengers <= self.MAXSEAT-self.currSeat):
            self.currSeat += passengers
            return 0
        else:
            leftover = passengers - (self.MAXSEAT - self.currSeat)
            self.currSeat = self.MAXSEAT
            return leftover

    def unloadPassengers(self):
        self.currSeat = 0


# classe per STANDINGPOINTS

class StandPoint:
    node_id = 0 # nodo di riferimento per lo STANDINGPOINT
    # numero massimo di BUS che possono sostare 
    # nello STANDINGPOINT (inizializzato nel costruttore)
    maxbus = 1 
    currbus = 0 # BUS attualmente assegnati allo STANDINGPOINT
    pickup_list = None # lista dei PICKUPPOINTS che lo STANDINGPOINT deve servire

    def __init__(self, node_id, maxbus): #costruttore
        self.maxbus = maxbus
        self.node_id = node_id
        self.pickup_list = list()
        self.bus_list = list()

    def add_pickup(self, pick):
        self.pickup_list.append(pick)

    def get_pickup(self):
        return self.pickup_list

    # aggiunta e rimozione dei BUS viene fatto
    # in modo unitario

    def add_bus(self, bus):
        if self.currbus < self.maxbus:
            self.currbus += 1
            self.bus_list.append(bus)
            return self.currbus
        return -1

    def remove_bus(self, bus):
        if(self.currbus > 0):
            self.currbus -= 1
            self.bus_list.remove(bus)
            return self.currbus
        return -1

    def get_currbus(self):
        return self.currbus

    def get_node_id(self):
        return self.node_id

# classe PICKUPPOINT

class PickupPoint:
    node_id = 0 # nodo di riferimento del PICKUPPOINT
    people = 0 # persone ferme alla fermata del PICKUPPOINT
    best_standing = 0 # STANDINGPOINT che serve il PICKUPPOINT

    def __init__(self, node_id, people):
        self.people = people
        self.node_id = node_id

    def set_people(self, value):
        if(value > 0):
            self.people = value

    def set_best_standing(self, value):
        self.best_standing = value

    def get_best_standing(self):
        return self.best_standing

    def get_people(self):
        return self.people

    def get_node_id(self):
        return self.node_id


# MAIN

if __name__ == '__main__':
    g = Graph() # inizializzazione grafo

    for i in range(1, 37): # creazione nodi
        g.add_vertex(i)

    file = open("Map.txt") # inserimento archi da file
    for line in file:
        arc = line.split(",")
        n1 = int(arc[0])
        n2 = int(arc[1])
        n3 = int(arc[2])
        g.add_edge(n1, n2, n3)

    g.print_graph_data() # stampa grafo
    
    # inizializzazione BUS, STANDINGPOINT, PICKUPPOINT
    n = 10  
    busses = {}
    for i in range(n):
        b = Bus(i)
        busses[i] = b

    standing = {}
    for i in [8, 17, 26, 35]:
        standing[i] = StandPoint(i, 5)

    pickup = {}
    for i in [1, 6, 10, 13, 15, 20, 24, 28, 32, 36]:
        p = PickupPoint(i, random.randint(0, 10))
        pickup[i] = p
    
    # STAMPA STATO INIZIALE
    
    print("Initial state: \n")
    print("State of the standing point:")
    for k in standing:
        print("\tStanding point: " + str(standing[k].get_node_id()) + " Number of busses: " + str(standing[k].get_currbus()))
    print("\nState of the pickup points:")
    for k in pickup:
        print("\tPickup point: " + str(pickup[k].get_node_id()) + " Number of people: " + str(pickup[k].get_people()))
    
    # FINE STAMPA STATO INIZIALE
    
    
    # questo ciclo determina lo STANDINGPOINT migliore per ogni PICKUPPOINT
    # applicando Dijkstra, partendo dagli STANDINGPOINT verso i PICKUPPOINT
    for k in pickup:
        p = g.get_vertex(k)
        print("\nCurrent pickup point: " + str(p))
        minpath = []
        min_weight = sys.maxsize
        min_standing = 0
        for i in standing:
            s = g.get_vertex(i)
            path = g.dijkstra(s, p)
            path_weight = p.get_distance()
            if path_weight < min_weight:
                minpath = path
                min_weight = path_weight
                min_standing = i
            g.reset_visited()
            g.reset_distance()
    
        #assegnazione PICKUPPOINT e STANDINGPOINT
        pickup[k].set_best_standing(min_standing)
        standing[min_standing].add_pickup(k)
        print("\nFor PickupPoint: " + str(k))
        print("\tBest standing_point: " + str(min_standing))
        print("\tBest path: " + str(minpath))
    
    # questo ciclo effettua la distribuzione ottima dei BUS sugli STANDINGPOINT
    # come criterio usa il numero di PICKUPPOINT assegnati allo STANDINGPOINT
    
    for j in standing:
        pick = len(standing[j].get_pickup());
        i = 0
        for k in busses:
            if(busses[k].get_standing_point() == 0):
                busses[k].set_standing_point(standing[j].get_node_id())
                standing[j].add_bus(busses[k])
                i += 1
                if(i == pick): break

    # STAMPA DELLO STATO
    
    print("\nBest pickup for each standing point:")
    for k in standing:
        print("\tStanding point: " + str(standing[k].get_node_id()) + " Pickup : " + str(standing[k].get_pickup()))
    print("\nBusses assigned for each standing point:")
    for k in busses:
        print("\tBus: " + str(busses[k].get_id()) + " Max Occupancy: " + str(busses[k].MAXSEAT) + " Position :" + str(busses[k].get_standing_point()))
    print("\nBest standing point for each pickup point:")
    for k in pickup:
        print("\tPickup point: " + str(pickup[k].get_node_id()) + " Best Standing: " + str(pickup[k].get_best_standing()))
    
    # FINE STAMPA DELLO STATO
    
    # SCELTA NAVETTA DI SUPPORTO
    # come caso di esempio è stato fissato che i seguenti PICKUPPOINT
    # chiedono supporto
    pick6 = PickupPoint(6, 4)
    pick28 = PickupPoint(28, 6)

    picks = {}
    picks[6] = pick6
    picks[28] = pick28
    
    # questo ciclo genera randomicamente il livello di occupazione
    # e la posizione dei BUS
    
    for k in busses:
        num_pepople = random.randint(0, 10)
        position = random.randint(1, 36)
        while position in [6, 28]:
            position = random.randint(1, 36)
        busses[k].loadPassengers(num_pepople)
        busses[k].updatePosition(position)

    # STAMPA POSIZIONE PARTENZA BUS

    print("\nBusses assigned for each standing point:")
    for k in busses:
        print("\tBus: " + str(busses[k].get_id()) + " Max Occupancy: " + str(busses[k].MAXSEAT) + " Position :" + str(busses[k].get_position()))

    # questo ciclo determina il miglior BUS da inviare per ogni PICKUPPOINT
    # che ha richiesto supporto usando Dijkstra da ogni BUS fino al PICKUPPOINT
    # rispettando la condizione che il BUS deve avere curr_seat >= people
    # (capienza attuale BUS >= persone in attesa alla fermata)

    for k in picks:
        p = g.get_vertex(k)
        print("\nCurrent pickup point: " + str(p))
        minpath = []
        min_weight = sys.maxsize
        min_standing = 0
        for i in busses:
            pasb = busses[i].get_passengers()
            peop = picks[k].get_people()
            if pasb >= peop:
                s = g.get_vertex(busses[i].get_position())
                path = g.dijkstra(s, p)
                path_weight = p.get_distance()
                if path_weight < min_weight:
                    minpath = path
                    min_weight = path_weight
                    min_bus = i
                g.reset_visited()
                g.reset_distance()
            
        # STAMPA BUS MIGLIORE PER OGNI PICKUPPOINT
        
        print("\tBus selected for support: " + str(min_bus))
        print("\t\tBus: " + str(busses[min_bus].get_id()) + " Max Occupancy: " + str(busses[min_bus].MAXSEAT) + " Position :" + str(busses[min_bus].get_position()))
