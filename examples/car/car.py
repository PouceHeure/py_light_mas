from py_light_mas.agent import Agent 
from py_light_mas.network import Network 
from py_light_mas.simulation import Simulation 
from py_light_mas.environnemnt import Environnemnt 


class RoadEnvironnemnt(Environnemnt):

    CELL_EMPTY = 0
    CELL_CAR = 1 
    CELL_OBSTACLE = 2

    def __init__(self,length_road,**kargs):
        super(RoadEnvironnemnt, self).__init__(**kargs)
        self._length_road = length_road
        self._road = self._init_road(length_road)

        self._car_position = 0

    def _init_road(self,length_road):
        return [RoadEnvironnemnt.CELL_EMPTY] * length_road + [RoadEnvironnemnt.CELL_OBSTACLE]

    def _update_road(self):
        self._road = self._init_road(self._length_road)
        self._road[self._car_position] = 1

    def get_road(self):
        return self._road

    def get_position(self):
        return self._car_position

    def move_car(self):
        self._car_position += 1 
        self._update_road()

    def _on_event_show(self):
        result = "" 
        for element in self._road: 
            if(element == RoadEnvironnemnt.CELL_EMPTY):
                result += "_"
            elif(element == RoadEnvironnemnt.CELL_CAR):
                result += "O"
            elif(element == RoadEnvironnemnt.CELL_OBSTACLE):
                result += "|"
        print(result)


class CarAgent(Agent): 

    def __init__(self,**kargs): 
        super(CarAgent, self).__init__(**kargs)

    def _on_event_new_tick(self,env):
        road = env.get_road()
        position = env.get_position()
        if(road[position + 1] == 0): 
            env.move_car()

class CarSimulation(Simulation):

    def __init__(self,**kargs):
        super(CarSimulation, self).__init__(**kargs)
        self._env = RoadEnvironnemnt(50)
        a1 = CarAgent(name="agent_a1")
        print(a1)
        self.add_agent(a1)

if __name__ == "__main__":
    sim = CarSimulation()
    sim.run(wait_s=0.1)

