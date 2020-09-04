
import abc 
import time 

from .environnemnt import Environnemnt

class Simulation: 

    def __init__(self,env=None): 
        self._env = env
        self._is_ok = True
        self._agents = []

    def add_agent(self,agent):
        self._agents.append(agent)

    def _run(self):
        for agent in self._agents: 
            agent.event_new_tick(self._env)
        self._env.event_new_tick()
        self._env.event_show()

    def run(self,wait_s=1):
        self._is_ok = True 
        while(self._is_ok):
            self._run()
            time.sleep(wait_s)
        