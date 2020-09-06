import time

from .agent import Agent
from .environnemnt import Environnemnt

class Simulation:
    """manage all events (agent/env.)
    """

    def __init__(self,env=None):
        self._env = env
        self._is_ok = True
        self._agents = []
        Agent.SIMULATION = self

    def add_agent(self,agent):
        self._agents.append(agent)

    def run(self):
        for agent in self._agents:
            agent.event_new_tick(self._env)
        if(self._env != None):
            self._env.event_new_tick()
            self._env.event_show()

    def run_loop(self,wait_s=1):
        self._is_ok = True
        while(self._is_ok):
            self.run()
            time.sleep(wait_s)