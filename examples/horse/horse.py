
"""
Simple horse example.
Build N agent (i.e. car), each agent have to run straight ahead until the next obstacle.
"""

import pygame

from py_light_mas.agent import Agent
from py_light_mas.network import Network
from py_light_mas.simulation import Simulation
from py_light_mas.environnemnt import Environnemnt


class RoadEnvironnemnt(Environnemnt):
    """
    Child class of Environnemnt
    """
    CELL_EMPTY = 0
    CELL_CAR = 1
    CELL_OBSTACLE = 2

    MAP_COLORS = {
        CELL_EMPTY: (255, 255, 255),
        CELL_CAR: (0, 0, 255),
        CELL_OBSTACLE: (255, 0, 0)
    }

    RECT_H = 10
    RECT_W = 10

    def __init__(self, length_road, **kargs):
        super(RoadEnvironnemnt, self).__init__(**kargs)
        self._length_road = length_road
        self._cars_position = {}

        self._road = None
        self._display = None

    def init_ui(self):
        n_cars = len(self._cars_position)
        self._display = pygame.display.set_mode(
            (RoadEnvironnemnt.RECT_W*self._length_road, RoadEnvironnemnt.RECT_H*n_cars))

    def init_road(self):
        board = []
        for _ in range(len(self._cars_position.keys())):
            board.append([RoadEnvironnemnt.CELL_EMPTY] *
                         (self._length_road - 1) + [RoadEnvironnemnt.CELL_OBSTACLE])
        self._road = board

    def _update_road(self):
        self.init_road()
        _i = 0
        for _, position in self._cars_position.items():
            self._road[_i][position] = 1
            _i += 1

    def add_car(self, car):
        self._cars_position[car] = 0

    def get_road(self, car):
        position = list(self._cars_position.keys()).index(car)
        return self._road[position]

    def get_position(self, car):
        return self._cars_position[car]

    def move_car(self, car):
        self._cars_position[car] += 1
        self._update_road()

    def _draw_rectangle(self, line, position, color):
        left = RoadEnvironnemnt.RECT_W*position
        top = RoadEnvironnemnt.RECT_H*line
        pygame.draw.rect(self._display, color,
                         (
                            left, top,
                            RoadEnvironnemnt.RECT_W, RoadEnvironnemnt.RECT_H
                         ))

    def on_event_show(self):
        for line in range(len(self._road)):
            road = self._road[line]
            for _i in range(len(road)):
                element = road[_i]
                color = RoadEnvironnemnt.MAP_COLORS[element]
                self._draw_rectangle(line, _i, color)


class CarAgent(Agent):

    def __init__(self, **kargs):
        super(CarAgent, self).__init__(**kargs)
        self._run = True

    def on_event_new_tick(self, env):
        import random
        road = env.get_road(self)
        position = env.get_position(self)
        v_rnd = random.randint(0, 10)
        next_cell = road[position + 1]
        if(self._run):
            if(next_cell == RoadEnvironnemnt.CELL_EMPTY and v_rnd < 5):
                print("move")
                env.move_car(self)
            elif(next_cell == RoadEnvironnemnt.CELL_OBSTACLE):
                print("win")
                self._network.broadcast_message(self, "win")
                self._run = False
        else:
            print("stop")

    def on_event_new_message(self, message):
        self._run = False

    def on_event_new_signal(self, signal):
        print(signal)

class HorseSimulation(Simulation):

    def __init__(self, length_road=20, **kargs):
        super(HorseSimulation, self).__init__(**kargs)
        self._env = RoadEnvironnemnt(length_road)
        network = Network("localhost")
        for _i in range(10):
            agent = CarAgent(name=f"agent_a{_i}")
            agent.connect(network)
            self._env.add_car(agent)

        self._env.init_ui()
        self._env.init_road()


if __name__ == "__main__":
    pygame.init()
    sim = HorseSimulation(length_road=30)

    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        sim.run()
        pygame.display.update()
        pygame.time.wait(100)
        i += 1
