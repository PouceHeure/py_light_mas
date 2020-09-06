import time
import functools
from concurrent import futures
import threading

from .agent import Agent
from .environnemnt import Environnemnt

class Simulation:
    """manage all events (agent/env.)
    """

    def __init__(self,env=None):
        self._execution = 1
        self._env = env
        self._is_ok = True
        self._agents = []
        Agent.SIMULATION = self

    def add_agent(self,agent):
        """add adgent to simulation list
        It's really important to add agent, because events agent can't be called

        Args:
            agent (Agent): agent to add
        """
        self._agents.append(agent)

    def run(self):
        """run only one time 
        """
        if(self._execution > 1):
            #TODO: fix this part
            ex = futures.ThreadPoolExecutor(max_workers=2)
            ex.map(functools.partial(Agent.event_new_tick, env=self._env), self._agents)
        else: 
            for agent in self._agents:
                agent.event_new_tick(self._env)
        if(self._env != None):
            self._env.event_new_tick()
            self._env.event_show()

    def run_loop(self,wait_s=1):
        """at each tick call run method

        Args:
            wait_s (int, optional): time in seconds between 2 ticks. Defaults to 1.
        """
        self._is_ok = True
        while(self._is_ok):
            self.run()
            time.sleep(wait_s)