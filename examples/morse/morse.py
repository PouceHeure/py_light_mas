import random  

from py_light_mas.message import Message, Signal
from py_light_mas.agent import Agent
from py_light_mas.network import Network
from py_light_mas.simulation import Simulation
from py_light_mas.environnemnt import Environnemnt

class WorldEnvironnment(Environnemnt):

    def __init__(self,grid_size,**kargs):
        super(WorldEnvironnment, self).__init__(**kargs)
    
    def on_event_show(self):
        pass 

MORSE_LANGUAGES = [".","_"]

class SenderAgent(Agent):

    def __init__(self, **kargs):
        super(SenderAgent, self).__init__(**kargs)
        self._address_teammate = None 

    def add_teammate(self,address):
        self._address_teammate = address
        
    def on_event_new_tick(self, env):
        if(self._address_teammate != None):
            
            length = random.randint(1,20)
            content = "".join(random.choices(MORSE_LANGUAGES,k=length))
            message = Message(sender=self._address,
                              dest=self._address_teammate,
                              content=content) 
            self.send_message(message)

    def on_event_new_message(self, message):
        print(message)

    def on_event_new_signal(self, signal):
        print(signal)

class ReplierAgent(Agent):

    def __init__(self, **kargs):
        super(ReplierAgent, self).__init__(**kargs) 
        
    def on_event_new_tick(self, env):
        pass 

    def on_event_new_message(self, message):
        print(message)
        content = f"ok {message.content}"
        self.reply_message(message,content)

    def on_event_new_signal(self, signal):
        print(signal)


class WorldSimulation(Simulation):
    def __init__(self,**kargs):
        super(WorldSimulation, self).__init__(**kargs)
        network_A = Network("team_A")
        network_B = Network("team_B")

        agent_A_01 = SenderAgent(name=f"agent_A_01")
        address_A_01 = agent_A_01.connect(network_A)

        agent_B_01 = ReplierAgent(name=f"agent_B_01")
        address_B_01 = agent_B_01.connect(network_B)
        
        agent_A_01.add_teammate(address_B_01)

if __name__ == "__main__":
    sim = WorldSimulation()
    sim.run_loop(wait_s=1.5)