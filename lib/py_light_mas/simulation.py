
import abc 
import time 

from .environnemnt import Environnemnt

class Simulation: 

    def __init__(self,env=None,wait_s=1): 
        self._env = env
        self._wait_s = wait_s
        self._is_ok = True  
        self._agents = []

    def add_agent(self,agent):
        self._agents.append(agent)

    @abc.abstractmethod
    def _run(self,env):
        pass 

    def run(self):
        self._is_ok = True 
        while(self._is_ok):
            for agent in self._agents: 
                agent.event_new_tick(self._env)
            self._run(self._env)
            self._env.event_new_tick()
            self._env.event_show()
            time.sleep(self._wait_s)
        