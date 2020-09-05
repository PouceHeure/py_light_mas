import pygame

from py_light_mas.agent import Agent 
from py_light_mas.network import Network 
from py_light_mas.simulation import Simulation 
from py_light_mas.environnemnt import Environnemnt 

class RoadEnvironnemnt(Environnemnt):

    CELL_EMPTY = 0
    CELL_CAR = 1
    CELL_OBSTACLE = 2

    MAP_COLORS = {
        CELL_EMPTY: (255,255,255),
        CELL_CAR: (0,0,255),
        CELL_OBSTACLE: (255,0,0)
    }

    rect_H = 10
    rect_W = 10

    def __init__(self,length_road,**kargs):
        super(RoadEnvironnemnt, self).__init__(**kargs)
        self._length_road = length_road
        self._cars_position = {}

    def init_ui(self):
        n_cars = len(self._cars_position)
        self._display = pygame.display.set_mode((RoadEnvironnemnt.rect_W*self._length_road
                                                ,RoadEnvironnemnt.rect_H*n_cars))
    def init_road(self):
        board = [] 
        for _ in range(len(self._cars_position.keys())):
            board.append([RoadEnvironnemnt.CELL_EMPTY] * (self._length_road -1) + [RoadEnvironnemnt.CELL_OBSTACLE])
        self._road = board 

    def _update_road(self):
        self.init_road()
        i = 0
        for _,position in self._cars_position.items():
            self._road[i][position] = 1
            i += 1

    def add_car(self,car):
        self._cars_position[car] = 0 

    def get_road(self,car):
        position = list(self._cars_position.keys()).index(car)
        return self._road[position]

    def get_position(self,car):
        return self._cars_position[car]

    def move_car(self,car):
        self._cars_position[car] += 1
        self._update_road()

    def _draw_rectangle(self,line,position,color):
        left = RoadEnvironnemnt.rect_W*position
        top = RoadEnvironnemnt.rect_H*line
        pygame.draw.rect(self._display,color,
                (left,top,
                 RoadEnvironnemnt.rect_W,RoadEnvironnemnt.rect_H)
        )

    def on_event_show(self):
        for line in range(len(self._road)):
            road = self._road[line]
            for i in range(len(road)):
                element = road[i] 
                color = RoadEnvironnemnt.MAP_COLORS[element]
                self._draw_rectangle(line,i,color)


class CarAgent(Agent): 

    def __init__(self,**kargs): 
        super(CarAgent, self).__init__(**kargs)
        self._run = True

    def on_event_new_tick(self,env):
        import random
        road = env.get_road(self)
        position = env.get_position(self)
        v_rnd = random.randint(0,10)
        next_cell = road[position + 1]
        if(self._run):
            if(next_cell == RoadEnvironnemnt.CELL_EMPTY and v_rnd < 5): 
                print("move")
                env.move_car(self)
            elif(next_cell == RoadEnvironnemnt.CELL_OBSTACLE):
                print("win")
                self._network.broadcast_message(self,"win")
                self._run = False 
        else: 
            print("stop")

    def on_event_new_message(self,message):
        self._run = False

class CarSimulation(Simulation):

    def __init__(self,length_road=20,**kargs):
        super(CarSimulation, self).__init__(**kargs)
        self._env = RoadEnvironnemnt(length_road)
        network = Network("localhost")
        for i in range(10):
            a1 = CarAgent(name=f"agent_a{i}")
            a1.connect(network)
            self._env.add_car(a1)

        self._env.init_ui()
        self._env.init_road()

if __name__ == "__main__":
    pygame.init()
    sim = CarSimulation(length_road=30)
    
    i = 0 
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        
        sim.run()
        pygame.display.update()
        pygame.time.wait(100)
        i += 1
    

