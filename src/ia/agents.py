import random
from enum import Enum
import networkx as nx
import ast
import numpy as np
import datetime


class Color(Enum):
    VERDE = 1
    AMARILLO = 2
    ROJO = 3

class Vehicle:
    """Representa los vehículos de la compañía"""
    
    def __init__(self, ID, capacity, total_km, risk_probability, logger, map, initial): #current_location: Dict, capacity: int, clients_on_board: int, initial_miles: float, std_dev: float, probability: float
        self.id = ID
        self.current_location = self.initial = initial
        self.days_off = 0 #disponibilidad del vehiculo. Si es > 0 representa los dias que no se usara
        self.capacity = capacity
        self.total_km = total_km
        self.km_traveled = 0
        self.route = None
        self.people_on_board = 0
        self.risk_probability = risk_probability
        self.speed = 0 #Representa los km/h
        self.taxes = 0        
        self.count_moves = 0 
        self.logger = logger
        self.free_pass = False
        self.free_pass_authority = False
        self.map = map
        self.last_stop = None
        self.turning_back = False    
        self.change_speed()
        self.principal_stops = []
        self.distance = 0 #es en km

    def __repr__(self) -> str:
        return f"{self.id}" 
    
    def __str__(self):
        return f"Vehículo {self.id}" #, Model: {self.model}>"
        
    def reset_vehicle(self):
        self.current_location = self.initial
        self.count_moves = 0
        self.free_pass = False
        self.free_pass_authority = False
        self.last_stop = None
        self.turning_back = False 
        self.change_speed()
        self.distance = 0

    def fixed(self):
        self.reset_vehicle()
        self.route = None
        self.total_km -= abs(int(random.gauss(0,0.1*self.total_km))) #CAMBIAR VALOR DE LA DESVIACION ESTANDAR

    def move(self, global_time):
        """Mueve al vehículo a su próximo destino"""
        speed = self.speed
        self.count_moves += 1
        cost = self.map[ast.literal_eval(self.current_location.id)][ast.literal_eval(self.route[self.count_moves].id)]['weight']
        self.km_traveled += round(cost/1000,2) #convierto el costo de las aristas que estan en metros a km
        self.km_traveled = round(self.km_traveled,2)
        self.distance += round(cost/1000,2)
        self.distance = round(self.distance,2)
        self.change_speed()        
        origin = self.current_location
        self.current_location = self.route[self.count_moves]

        return speed, cost      
    
    def change_speed(self):
        self.speed = int(random.gauss(45, 10))        
    
    def pass_AMARILLO(self) -> bool:
        """Calcula la probabilidad de que el vehiculo se pase o no la amarilla del semaforo.
        Devuelve True o False."""
        return random.random() < self.risk_probability
    
    
    #! Devuelve la cantidad de pasajeros que pudo recoger en esa parada (ARREGLAR)
    def load(self, global_time):
        """Modifica la cantidad de pasajeros que quedan en la parada y la
         capacidad disponible en el vehículo"""             
        people = min(self.current_location.people, self.capacity - self.people_on_board)
        self.last_stop = self.current_location
        self.people_on_board += people
        self.current_location.people -= people 


        if self.capacity == self.people_on_board:
            self.turning_back = True
            route = self.route.copy()
            self.route = self.go_to_depot()
            self.logger.log(f"{str(datetime.timedelta(seconds = global_time))} {self} está lleno, cambia su ruta de:\n {route} \n -> \n {self.route} para descargar a las personas y poder seguir recogiendo.\n")
        
        return people
        
    
    def unload(self, global_time):
        '''Descarga a los pasajeros en la posicion current_stop'''
        people = self.people_on_board
        self.people_on_board = 0
        return people

    def at_semaphore(self, global_time):
        wait = 0
        semaphore = self.current_location.semaphore        
        color = semaphore.state
            
        semaphore_time_left = sum(semaphore.color_range) - semaphore.time_color
        if color == Color.AMARILLO:
            if self.pass_AMARILLO():# no hace nada
                self.logger.log(f"{str(datetime.timedelta(seconds = global_time))} {self} no paró en el {semaphore}.\n")
            else:
                wait = semaphore_time_left
                self.logger.log(f"{str(datetime.timedelta(seconds = global_time))} {self} paró {wait} segundos en el {semaphore}.\n")

        elif color == Color.ROJO:
            wait = semaphore_time_left
            self.logger.log(f"{str(datetime.timedelta(seconds = global_time))} {self} paró {wait} segundos en el {semaphore}.\n")
        
        else:
            self.logger.log(f"{str(datetime.timedelta(seconds = global_time))} {self} pasó el {semaphore}.\n")

        return wait
          

    def go_to_depot(self):
        stops = [self.current_location, self.route[len(self.route)-1]]        
        path = self.__get_complete_route(stops)
        path =self.route[0:self.count_moves + 1] + path[:len(path)-1] + list(reversed(path)) + self.route[self.count_moves:]
        return path


    def change_route(self):
       
        start = self.count_moves
        stops = [self.route[start], self.route[start+1]]   
                  
        origin= ast.literal_eval(self.current_location.id)
        not_available = ast.literal_eval(self.route[start+1].id)

        temp = self.map[origin][not_available]['weight']
        self.map[origin][not_available]['weight'] = float('inf')     

        
        path = self.__get_complete_route(stops)

        path = self.route[0:start+1] + path +  self.route[start+2:]

        self.map[origin][not_available]['weight']=temp

        return path
    
    def broken(self, global_time):
        self.km_traveled = round(1/4 * self.total_km,2) 
        time_h = random.randint(30, 60) #Espera de 30min a 1h
        time_broken = 60*time_h #convertir el tiempo de min a segundos
        cost = time_h*2 + 80 # el costo del servicio. Si se demora 1h cuesta 200 pesos
        self.logger.log(f"{str(datetime.timedelta(seconds = global_time))} {self} se rompió en la {self.current_location}.\n")
        return time_broken, cost

  
    # def plan(self):

    #     if self.turning_back and self.current_location == self.last_stop and self.capacity != self.people_on_board:
    #         self.turning_back = False

    #     if self.current_location.authority != None and not self.free_pass_authority:
    #         self.free_pass_authority = True
    #         return 'at_authority'
    #     elif self.current_location in self.principal_stops and ((self.current_location.people > 0 and self.people_on_board != self.capacity and not self.turning_back) or (self.turning_back and self.current_location.people > 0 and self.people_on_board != self.capacity and self.current_location == self.last_stop)):
    #         return 'load'
    #     elif self.current_location == self.route[len(self.route)-1] and self.people_on_board > 0:
    #         return 'unload'
    #     elif self.current_location.semaphore != None and not self.free_pass:
    #         self.free_pass = True
    #         return 'at_semaphore' 

    #     elif (self.count_moves+1)< len(self.route) and self.km_traveled + (self.map[ast.literal_eval(self.current_location.id)][ast.literal_eval(self.route[self.count_moves+1].id)]['weight'])/1000 > self.total_km:
    #         return 'broken'       
    #     else:
    #         self.free_pass_authority = False
    #         self.free_pass = False
    #         return 'move'


    def goal_test(self):

        if self.current_location != self.route[len(self.route)-1] or self.people_on_board > 0:
            return False

        for node in self.principal_stops:
            if node.people > 0:
                return False

        return True

    def __get_complete_route(self, stops):

        """Obtiene la ruta completa a partir de una secuencia de paradas"""

        path = []
        nodes = nx.get_node_attributes(self.map,'value')
        
        for i in range(len(stops)-1):
            shortest_path = nx.shortest_path(self.map,ast.literal_eval(stops[i].id),ast.literal_eval(stops[i+1].id),weight='weight')
            for j in range(1,len(shortest_path)):
                path.append(nodes[shortest_path[j]])

        return path
        
class Semaphore:
    """Representa los semaforos en el mapa"""

    def __init__(self, position):
        self.position =position
        self.state = Color.VERDE
        self.color_range = [random.randint(1,30), 3, random.randint(1,30)]
        self.time_color = 0
    
    def __repr__(self) -> str:
        return f"Semáforo {self.position}"
    
    def __str__(self) -> str:
        return f"Semáforo con luz {self.state.name} en la posición {self.position} del mapa"
    
    def update_color(self, global_time):
        self.time_color = global_time % sum(self.color_range)
        if self.time_color <= self.color_range[0]:
            self.state = Color.VERDE
        elif self.time_color >self.color_range[0] and (self.time_color < self.color_range[0] + self.color_range[1]):
            self.state = Color.AMARILLO
        else:
            self.state = Color.ROJO
           
class Company:
    """Representa la compañia de transporte"""

    def __init__(self, name: str, budget: float, map, clients, vehicles, depot, logger):
        self.name = name
        self.depot = depot # MapNode con la localizacion del deposito de la compania
        self.clients = clients # lista de diccionarios de la forma {client_name:[[MapNodes],MapNode]}
        self.routes = {} #a cada vehiculo se le asigna una ruta
        self.budget = budget # presupuesto disponible
        self.vehicles = vehicles # lista de vehiculos q tiene la compañia
        self.map = map
        self.logger=logger
        self.vehicle_client = {}
        self.vehicle_principal_stops = {}
        self.vehicle_route = []
        self.substitute = {}# diccionario de vehiculo que esta sustituyendo al que esta en mantenimiento de la forma {id_vehiculo en mantenimiento:[id vehiculo sustituto, ruta vehiculo sustituto, client_id]}
        self.available_vehicles = [] # vehiculos que no estan asignados
        self.assign()

        self.logger.log(f"{self} realizó las siguientes asignaciones:\n Cliente - Vehículo\n {self.vehicle_client}\n\n  Vehículo - Paradas\n {self.vehicle_principal_stops}.\n")
        
        self.logger = logger

    def __repr__(self) -> str:
        return f"{self.name}"
    
    def __str__(self) -> str:
        return f"{self.name}"

    def assign(self):

        self.__assign_vehicle_to_client()
        self.__assign_stops_to_all_vehicles()
        self.__check_assign_vehicles()

        self.__get_route_of_vehicles()

    def __check_assign_vehicles(self):

        not_assigned_vehicles = []

        for v in self.vehicle_principal_stops.keys():
            if len(self.vehicle_principal_stops[v]) == 2:
                not_assigned_vehicles.append(v)
        
        i = 0
        while i < len(not_assigned_vehicles):
            self.vehicle_principal_stops.pop(not_assigned_vehicles[i])
            i += 1


        if len(not_assigned_vehicles) > 0:
            for value in self.vehicle_client.values():
                for v in value:
                    if v.id in not_assigned_vehicles:
                        value.remove(v)

        assign_vehicles = []

        for v in self.vehicle_client.values():
            assign_vehicles += v

        for v in self.vehicles:
            if v not in assign_vehicles:
                self.available_vehicles.append(v)


                                            
    def __assign_stops_to_all_vehicles(self):

        for c in self.vehicle_client.keys():
            vehicles = self.vehicle_client[c]
            stops = self.clients[c][0] + [self.depot] + [self.clients[c][1]] 
            self.__assign_stops_to_vehicle(vehicles,stops)

    def __assign_stops_to_vehicle(self, vehicles, stops):

        """Asigna vehiculos a rutas de un cliente. 
        Retorna diccionario de la forma {vehiculo.id:[lista de paradas]}"""
        
        vehicle_capacities = [v.capacity for v in vehicles]
        client_demands = [s.people for s in stops]

        assignations, cost = SimulatedAnnealingRouteToVehicle(vehicle_capacities, client_demands).run()

        for i in range(len(assignations)):
            if assignations[i] == 1:
                vehicle = vehicles[int(i/len(stops))]
                stop = stops[i%len(stops)]
                
                if vehicle.id in self.vehicle_principal_stops.keys():
                    self.vehicle_principal_stops[vehicle.id].append(stop)
                else:
                    self.vehicle_principal_stops.update({vehicle.id:[stop]})

    
    def __assign_vehicle_to_client(self):
        """Asigna a cada cliente los vehiculos 
        necesarios para recoger a todas las personas en las paradas. 
        Retorna diccionario de la forma {client_name:[lista vehiculos]}"""

        vehicles_capacities = []
        clients_demands = []
        
        for v in self.vehicles:
            vehicles_capacities.append(v.capacity)

        for c in self.clients.values():
            clients_demands.append(sum([m.people for m in c[0]]))            

        assignations, cost = SimulatedAnnealingVehiclesToClients(vehicles_capacities,clients_demands).run()
        
        for i in range(len(assignations)):
            if assignations[i] == 1:
                vehicle = self.vehicles[int(i/len(self.clients))]
                client = list(self.clients.keys())[i%len(self.clients)]
                
                if client in self.vehicle_client.keys():
                    self.vehicle_client[client].append(vehicle)
                else:
                    self.vehicle_client.update({client:[vehicle]})



    def __get_route_of_vehicles(self):

        for v in self.vehicle_principal_stops.keys():
            distances = self.__get_distance_beetween_stops(self.vehicle_principal_stops[v])
            route = AntColony(distances, 5, 100, 0.95, alpha=1, beta=1, delta_tau = 2).run()[0]
            route_nodes = []
            for x,y in route:
                route_nodes.append(self.vehicle_principal_stops[v][x])
            route_nodes.append(self.vehicle_principal_stops[v][len(self.vehicle_principal_stops[v])-1])

            route_nodes = self.__get_complete_route(route_nodes)
            vehicle = self.__get_vehicle_from_id(v)
            self.vehicle_route.append({v: vehicle ,'R' + v:route_nodes})
            vehicle.principal_stops=self.vehicle_principal_stops[v]
     

    def __get_distance_beetween_stops(self, stops):
        
        distances = [[0 for i in range(len(stops))] for j in range(len(stops))]

        for i in range(len(stops)):
            for j in range(len(stops)):
                if i != j:
                    distances[i][j]=nx.shortest_path_length(self.map,source=ast.literal_eval(stops[i].id),target=ast.literal_eval(stops[j].id),weight='weight')
                else:
                    distances[i][j] = 0

        
        return np.array(distances)


    def __get_complete_route(self, stops):

        """Obtiene la ruta completa a partir de una secuencia de paradas"""

        path = [stops[0]]
        nodes = nx.get_node_attributes(self.map,'value')
        
        for i in range(len(stops)-1):
            shortest_path = nx.shortest_path(self.map,ast.literal_eval(stops[i].id),ast.literal_eval(stops[i+1].id),weight='weight')
            for j in range(1,len(shortest_path)):
                path.append(nodes[shortest_path[j]])

        return path

    def __get_vehicle_from_id(self, vehicle_id):
        """Devuelve el objeto vehiculo a partir de su id"""

        for v in self.vehicles:
            if v.id == str(vehicle_id):
                return v
    
    def __get_route_from_id(self, route_id):
        """Devuelve el objeto vehiculo a partir de su id"""

        for item in self.vehicle_route:
            if str(route_id) in item.keys():
                return item[str(route_id)]

    def start_route(self, vehicle_id, route_id):
        vehicle = self.__get_vehicle_from_id(vehicle_id)
        vehicle.reset_vehicle()
        self.logger.log(f"{vehicle} comenzó su ruta.\n")
        vehicle.route = self.__get_route_from_id(route_id)
        return vehicle
         
        
    def buy_vehicle(self, new_vehicle: Vehicle, cost: int):
        self.logger.log(f"{self} compró un nuevo {new_vehicle} a {cost} pesos.\n")
        self.vehicles.append(new_vehicle)
        self.budget -= cost
    
    def pay_taxes(self, vehicle_id): 
        """Paga las multas de los vehiculos en esa ruta si hubo y tambien cobra al cliente por haber
        pedido el servicio de taxis."""
        vehicle = self.__get_vehicle_from_id(vehicle_id)
        result = vehicle.taxes
        self.logger.log(f"{self} tuvo perdidas de {result} pesos en multas por el {vehicle}.\n")
        vehicle.taxes = 0
        income = 10 * vehicle.capacity * len(vehicle.route) # El pago por los servicios
        gas = round(25*(vehicle.distance/15),2) # Cada 15km gasta 1 litro de gasolina que cuesta 25 pesos.
        self.budget +=income
        self.budget = round(self.budget,2)
        self.logger.log(f"{self} tuvo ganancias de {income} pesos por los servicios prestados por el {vehicle}.\n")
        self.logger.log(f"{self} gastó {gas} pesos en la gasolina del {vehicle} que recorrió {round(vehicle.distance,2)} km.\n")
        self.budget = self.budget - (result + gas)

    def check_vehicle(self, vehicle_id):
        vehicle = self.__get_vehicle_from_id(vehicle_id)
        if vehicle.km_traveled >= (3/4) * vehicle.total_km:
            vehicle.days_off = random.randint(2,4)
            self.budget -= 500
            self.find_replacement(vehicle)
            self.logger.log(f"{vehicle} debe ir al mantenimiento por {vehicle.days_off - 1} días.\n")
            self.logger.log(f"Gastos:{500}\n")
        else:
            self.logger.log(f"{vehicle} está en perfectas condiciones.\n")

        return vehicle.days_off        

    def check_maintenance(self):
        """Se chequean los vehiculos que estan en mantenimiento para reincorporarlos a sus rutas si el cliente tenia mas
        de 1 vehiculo."""
        for v in self.vehicles:
               if v.days_off > 0:
                    v.days_off -= 1
                    if v.days_off == 0:
                        v.fixed()
                        if (v.id in self.vehicle_principal_stops.keys()):
                            substitute =self.substitute.pop(v.id)
                            substitute_vehicle= substitute[0]
                            substitute_route = substitute[1]
                            substitute_client = substitute[2]
                            substitute_vehicle.route = substitute_route
                            self.vehicle_client[substitute_client].append(v)
                            stops = []

                            for s in substitute_vehicle.principal_stops:
                                if s not in v.principal_stops:
                                    stops.append(s)
                            stops = stops + v.principal_stops[len(v.principal_stops)-2:]

                            substitute_vehicle.principal_stops = stops

                            for item in self.vehicle_route:
                                 if substitute_vehicle.id in item.keys():
                                     item.pop(f'R{substitute_vehicle.id}')
                                     item[f'R{substitute_vehicle.id}'] = substitute_vehicle.route
                                     break
                        else:
                            self.available_vehicles.append(v)

                       

    def find_replacement(self, vehicle: Vehicle):
        """Cuando un vehiculo se manda a mantenimiento buscar sustituto si se puede."""
        #Ver si hay vehiculos disponibles: Son los vehiculos que estan en self.vehicles que no estan
        # en self.vehicles_client:
        selected_v = None
        clientid = 0
        #Encontrar el cliente del vehiculo
        for c in self.vehicle_client.keys():
            for v in self.vehicle_client[c]:#Recorrer la lista de vehiculos del cliente
                if vehicle.id == v.id:
                    clientid = c
                    break
        

        if len(self.available_vehicles) != 0:
            max_capacity = 0
            #Selecciono el vehiculo de mayor capacidad entre los disponibles
            for v in self.available_vehicles: 
                if max_capacity < v.capacity:
                    selected_v = v
                    max_capacity = selected_v.capacity
            selected_v.route = vehicle.route
            vehicle.route = []
            selected_v.principal_stops = vehicle.principal_stops
            vehicle.principal_stops = []           
            self.available_vehicles.remove(selected_v)
            self.vehicle_client[clientid].remove(vehicle)#le quito el vehiculo al cliente y le añado el nuevo
            self.vehicle_client[clientid].append(selected_v)
            self.vehicle_principal_stops[selected_v.id] = self.vehicle_principal_stops.pop(vehicle.id)
            
            
            # busco el diccionario que tenga vehicle.id y lo sustituyo por selected_v.id
            for item in self.vehicle_route:
                if vehicle.id in item.keys():
                    item.pop(vehicle.id)
                    route = item.pop(list(item.keys())[0])
                    item.update({selected_v.id : selected_v})
                    item.update({'R'+ selected_v.id: route})
                    break
            
            # ver si vehicle esta en sustituto, si es asi, cambiar vehicle por selected_v
            for v in self.substitute.keys():
                if self.substitute[v][0].id == vehicle.id:
                    self.substitute[v][0] = selected_v
                    


        # Ver si el cliente tiene asignado otros vehiculos
        elif len(self.vehicle_client[clientid]) > 1:
            selected_v = vehicle
            while selected_v.id == vehicle.id:
                selected_v = random.choice(self.vehicle_client[clientid])
            selected_v.route = self.merge(selected_v, vehicle)
            route_selected_v = None
            for item in self.vehicle_route:
                if selected_v.id in item.keys():
                    route_selected_v = item.pop(f'R{selected_v.id}')
                    item[f'R{selected_v.id}'] = selected_v.route
                    break
            self.substitute.update({f'{vehicle.id}':[selected_v,route_selected_v,clientid]})
            self.vehicle_client[clientid].remove(vehicle)
            
        ## Ver si la compañia tiene presupuesto para comprar otro vehiculo(1500 pesos)
        elif self.budget - 1500 > 0:
            selected_v = Vehicle(f'V{len(self.vehicles) + 1}', vehicle.capacity, vehicle.total_km, vehicle.risk_probability, Logger(), self.map, self.depot)
            self.buy_vehicle(selected_v,1500)
            selected_v.route = vehicle.route
            vehicle.route = []
            selected_v.principal_stops = vehicle.principal_stops
            vehicle.principal_stops = []
            self.vehicle_client[clientid].remove(vehicle)#le quito el vehiculo al cliente y le añado el nuevo
            self.vehicle_client[clientid].append(selected_v)                    
            self.vehicle_principal_stops[selected_v.id] = self.vehicle_principal_stops.pop(vehicle.id)
            # busco el diccionario que tenga vehicle.id y lo sustituyo por selected_v.id
            for item in self.vehicle_route:
                if vehicle.id in item.keys():
                    item.pop(vehicle.id)
                    route = item.pop(list(item.keys())[0])
                    item.update({selected_v.id : selected_v})
                    item.update({'R'+ selected_v.id: route})
                    break

            # ver si vehicle esta en sustituto, si es asi, cambiar vehicle por selected_v
            for v in self.substitute.keys():
                if self.substitute[v][0].id == vehicle.id:
                    self.substitute[v][0] = selected_v
           

    def merge(self, new_vehicle, old_vehicle):
        stops_new = self.vehicle_principal_stops[new_vehicle.id]
        stops_old = self.vehicle_principal_stops[old_vehicle.id]

        stops = stops_new[:len(stops_new)-2] + stops_old

        new_vehicle.principal_stops = stops

        distances = self.__get_distance_beetween_stops(stops)
        route = AntColony(distances, 5, 100, 0.95, alpha=1, beta=1, delta_tau = 2).run()[0]
        route_nodes = []
        for x,y in route:
            route_nodes.append(stops[x])
        route_nodes.append(stops[len(stops)-1])
        route_nodes = self.__get_complete_route(route_nodes)
        
        return route_nodes


    def plan(self):

        plans=[]

        for a in self.vehicle_route:            
            v,r = a.keys()
            if a[v].days_off == 0:

                new_plan = PlanningProblem(initial = f'~Done({v},{r}) & ~Checked({v}) & ~Payed({v})',
                                            goals = f'Checked({v})',
                                            actions = [Action('start_route(c,v,r)',
                                                                precond='~Done(v,r) & ~Checked(v) & ~Payed(v)',
                                                                effect='Done(v,r) & EndRoute(v)',
                                                                domain='Vehicle(v) & Route(r) & Company(c)'),
                                                        Action('check_vehicle(c,v)',
                                                                precond='EndRoute(v) & Payed(v) & ~Checked(v)',
                                                                effect='Checked(v)',
                                                                domain='Vehicle(v) & Company(c)'),
                                                        Action('pay_taxes(c,v)',
                                                                precond='~Checked(v) & EndRoute(v) & ~Payed(v)',
                                                                effect='Payed(v)',
                                                                domain='Vehicle(v) & Company(c)')

                                                        ],
                                            agent=self,
                                            domain=f'Vehicle({v}) & Route({r}) & Company({self.name})')
                plans.append(new_plan)

        return plans

    def bankruptcy(self):
        return self.budget <= 0