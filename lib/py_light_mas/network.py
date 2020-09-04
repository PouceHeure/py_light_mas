
from .message import Message


class Network: 

    def __init__(self,name):
        self._name = name 
        self._number_connections = 0 
        self._agents = {}
    
    def get_agent(self,address):
        if(address in self._agents):
            return self._agents[address]
        return None 

    def get_name(self):
        return self._name 

    def _generator_address(self,id_connection): 
        return f"10.5.10.{id_connection}" 

    def _allocate_address(self,address,agent):
        if(not address is self._agents):
            self._agents[address] = agent
            return True 
        return False 

    def register_agent(self,agent): 
        id_connection = self._number_connections 
        address = self._generator_address(id_connection)
        if(self._allocate_address(address,agent)): 
            self._number_connections += 1 
            return address
        return None

    def send_message(self,message): 
        get_to_agent_adress = message.agent_to
        get_to_agent = self.get_agent(get_to_agent_adress) 
        get_to_agent.event_new_message(message)

    def broadcast_message(self,sender,content):
        for address,agent in self._agents.items():
            if(agent != sender):
                m = Message(sender=sender.get_address(),dest=address,content=content)
                self.send_message(m)