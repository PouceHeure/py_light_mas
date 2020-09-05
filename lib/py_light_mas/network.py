
from .message import Message, Signal



class Network: 

    GOBAL_NETWORK = {}

    def __init__(self,name):
        self._name = name 
        self._number_connections = 0 
        self._address_agents = {}

        Network.GOBAL_NETWORK[name] = self 
    
    def get_agent(self,address):
        domain, _  = self._deserialize_address(address)
        network = Network.GOBAL_NETWORK[domain]
        if(address in network._address_agents):
            return network._address_agents[address]
        return None 

    def get_name(self):
        return self._name 
    
    def _generator_address(self,domain,id_connection): 
        return f"{domain}/10.3.5.{id_connection}" 

    def _deserialize_address(self,address_str): 
        address_split = address_str.split("/")
        domain = address_split[0]
        address = address_split[1]
        return domain,address

    def _allocate_address(self,address,agent):
        if(not address is self._address_agents):
            self._address_agents[address] = agent
            return True 
        return False 

    def register_agent(self,agent): 
        id_connection = self._number_connections 
        address = self._generator_address(self._name,id_connection)
        if(self._allocate_address(address,agent)): 
            self._number_connections += 1 
            return address
        return None

    def send_message(self,message): 
        get_to_agent_adress = message.agent_to
        get_to_agent = self.get_agent(get_to_agent_adress) 
        get_to_agent.event_new_message(message)

    def send_signal(self,signal): 
        get_to_agent_adress = signal.agent_to
        get_to_agent = self.get_agent(get_to_agent_adress) 
        get_to_agent.event_new_signal(signal)

    def broadcast_message(self,sender,content):
        for address,agent in self._address_agents.items():
            if(agent != sender):
                m = Message(sender=sender.get_address(),dest=address,content=content)
                self.send_message(m)


    def __repr__(self): 
        return f"://{self._name}"