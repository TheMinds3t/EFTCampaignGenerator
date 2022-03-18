import config
import game_data;

import json 
import random

# Load missions from json file
mission_file = open("missions.json","r")
mission_list = json.load(mission_file)
mission_file.close()

# Structure to store all data related to an individual campaign, can be seeded
class Campaign:
    def __init__(self,size:int,seed:int,trader_levels,labs_final:bool=True,fence_allowed:bool=False):
        self.seed = seed
        random.seed(seed)

        # Reference to the maps in the game
        locations = game_data.map_list()

        # Generate start, end and full path.
        self.start_map = locations[random.randint(0,len(locations)-1)]
        self.end_map = locations[random.randint(0,len(locations)-1)]
        self.full_path = get_path_between(self.start_map,self.end_map)

        # If labs is set to destination only or the size of the above selection doesn't match the parameter
        while (self.start_map == self.end_map) or len(self.full_path) != size or (self.start_map == "The Lab" and labs_final == False):
            self.start_map = locations[random.randint(0,len(locations)-1)]
            self.end_map = locations[random.randint(0,len(locations)-1)]
            self.full_path = get_path_between(self.start_map,self.end_map)

        # Generate missions
        self.mission_pri = mission_list["Primary"][self.end_map][random.randint(0,len(mission_list["Primary"][self.end_map])-1)]
        self.mission_sec = mission_list["Secondary"][random.randint(0,len(mission_list["Secondary"])-1)]

        # Generate traders and trader levels
        trader_list = game_data.trader_list()
        self.trader_list = [] 
        self.trader_levels = []

        while len(self.trader_list) != len(self.full_path)-1:
            new_trader = trader_list[random.randint(0,len(trader_list)-1)]

            while new_trader in self.trader_list or (new_trader == "Fence" and fence_allowed == False):
                new_trader = trader_list[random.randint(0,len(trader_list)-1)]
                
            self.trader_list.append(new_trader)
            trader_level = random.random()

            # All trader levels in config are technically part of the same RNG roll
            if trader_level < trader_levels[0]:
                self.trader_levels.append(4)
            elif trader_level < trader_levels[1]:
                self.trader_levels.append(3)
            elif trader_level < trader_levels[2]:
                self.trader_levels.append(2)
            else:
                self.trader_levels.append(1)



# Function to find the shortest
# path between two nodes of a graph
def BFS_SP(graph, start:str, goal:str):
    explored = []
     
    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]
     
    # If the desired node is
    # reached
    if start == goal:
        return
     
    # Loop to traverse the graph
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]
         
        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]
             
            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                 
                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    # print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)
 
    return -1 

def get_path_between(location_1: str, location_2: str):
    return BFS_SP(game_data.map_graph(),location_1,location_2)
