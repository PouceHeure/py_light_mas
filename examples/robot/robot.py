import pygame

from py_light_mas.agent import Agent
from py_light_mas.network import Network
from py_light_mas.simulation import Simulation
from py_light_mas.environnemnt import Environnemnt

class GridEnvironnemnt(Environnemnt):

    CELL_EMPTY = 0
    CELL_RESOURCE = 1
    CELL_ROBOT = 2
    CELL_ROBOT_CURRENT = 3

    RECT_H = 10
    RECT_W = 10

    MAP_COLORS = {
        CELL_EMPTY: (255, 255, 255),
        CELL_RESOURCE: (0, 0, 255),
        CELL_ROBOT: (255, 0, 0), 
        CELL_ROBOT_CURRENT: (0,0,0)
    }

    def __init__(self,grid_size,**kargs):
        super(GridEnvironnemnt, self).__init__(**kargs)
        self._grid_size = grid_size
        self._grid = self._init_grid(grid_size)
        self._display = self._init_ui(grid_size)
        self._agents_position = {}

    def _init_grid(self,grid_size,percent_resource=0.3):
        grid = []
        for _ in range(grid_size):
            line = []
            for _ in range(grid_size):
                line.append(GridEnvironnemnt.CELL_EMPTY)
            grid.append(line)
        nb_cells_resource = int(grid_size*grid_size*percent_resource)

        cells_fill = 0 
        import random
        while(cells_fill < nb_cells_resource): 
            i = random.randint(0,grid_size-1)
            j = random.randint(0,grid_size-1)
            if(grid[i][j] == GridEnvironnemnt.CELL_EMPTY): 
                grid[i][j] = GridEnvironnemnt.CELL_RESOURCE
                cells_fill += 1

        return grid

    def _init_ui(self,grid_size): 
        display = pygame.display.set_mode(
            (GridEnvironnemnt.RECT_W*grid_size, GridEnvironnemnt.RECT_H*grid_size))
        return display

    def add_robot(self,robot_agent):
        import random
        i = random.randint(0,self._grid_size-1)
        j = random.randint(0,self._grid_size-1)
        position = [i,j]
        self._agents_position[robot_agent] = position


    def _draw_rectangle(self, line, position, color):
        left = GridEnvironnemnt.RECT_W*position
        top = GridEnvironnemnt.RECT_H*line
        pygame.draw.rect(self._display, color,
                         (
                             left, top,
                             GridEnvironnemnt.RECT_W, GridEnvironnemnt.RECT_H
                         )
                         )

    def get_cell(self,i,j): 
        if(i < 0 or j < 0 or i >= self._grid_size or j >= self._grid_size): 
            return None 
        return self._grid[i][j]

    def ask_env(self,agent):
        position = self._agents_position[agent]
        i = position[0]
        j = position[1]
        top = self.get_cell(i-1,j)
        bottom = self.get_cell(i+1,j)
        left = self.get_cell(i,j-1)
        right = self.get_cell(i,j+1)
        return [top,bottom,left,right]

    def ask_move_to_relatif(self,agent,move): 
        current_position = self._agents_position[agent]
        new_position = [sum(x) for x in zip(current_position, move)]
        if(not self.get_cell(new_position[0],new_position[1]) is None):
            self._agents_position[agent] = new_position
    
    def on_event_show(self):
        import copy 
        grid_with_robots = copy.copy(self._grid)

        for line in range(len(grid_with_robots)):
            road = grid_with_robots[line]
            for _i in range(len(road)):
                element = road[_i]
                color = GridEnvironnemnt.MAP_COLORS[element]
                self._draw_rectangle(line, _i, color)

        color = GridEnvironnemnt.MAP_COLORS[GridEnvironnemnt.CELL_ROBOT_CURRENT]
        for robot, positions in self._agents_position.items():  
            grid_with_robots[positions[0]][positions[1]] =  GridEnvironnemnt.CELL_ROBOT
            self._draw_rectangle(positions[0], positions[1],color)

class RobotAgent(Agent):

    def __init__(self, **kargs):
        super(RobotAgent, self).__init__(**kargs)
        
    def on_event_new_tick(self, env):
        cells = env.ask_env(self)
        actions = [[-1,0],
                   [+1,0],
                   [0,-1],
                   [0,+1]]

        action = None
        if(GridEnvironnemnt.CELL_RESOURCE in cells):
            index_resource = cells.index(GridEnvironnemnt.CELL_RESOURCE)
            action = actions[index_resource]
        else: 
            import random
            action = random.choice(actions)
        
        env.ask_move_to_relatif(self,action)

    def on_event_new_message(self, message):
        print(message)

    def on_event_new_signal(self, signal):
        print(signal)


class RobotSimulation(Simulation):
    def __init__(self, grid_size=100,number_robots=10, **kargs):
        super(RobotSimulation, self).__init__(**kargs)
        self._env = GridEnvironnemnt(grid_size)
        network = Network("localhost")

        for _i in range(number_robots):
            agent = RobotAgent(name=f"agent_a{_i}")
            agent.connect(network)
            self._env.add_robot(agent)


if __name__ == "__main__":
    pygame.init()
    sim = RobotSimulation(grid_size=30,number_robots=20)

    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        sim.run()
        pygame.display.update()
        #pygame.image.save(sim._env._display,f"img/{i}.png")
        pygame.time.wait(100)
        i += 1
