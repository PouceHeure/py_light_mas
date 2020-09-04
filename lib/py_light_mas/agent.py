import abc



class Agent: 

    COUNTER = 0

    def __init__(self,name=""): 
        self._name = name 
        self._address = None 
        self._network = None 
        self._aid = Agent.COUNTER
        Agent.COUNTER += 1

    def get_aid(self):
        return self._aid

    def get_addess(self): 
        return self._address

    def _guard_network(self,method_name): 
        if(self._network == None): 
            print(f"can't use {method_name} without connection")
            return False 
        return True 

    def connect(self,network): 
        address = network.register_agent(self)
        if(address != None): 
            print(f"success connection to: {network.get_name()}")
            self._network = network
        else: 
            print(f"fail to connect: {network.get_name()}")

        self._address = address
        return self._address

    def send_message(self,message): 
        if(not self._guard_network("send_message")): 
            return
        self._network.send_message(message)

    @abc.abstractmethod
    def _on_event_new_message(self,message):
        pass 

    @abc.abstractmethod
    def _on_event_new_tick(self,env): 
        pass 

    def event_new_message(self,message): 
        self._on_event_new_message(message) 

    def event_new_tick(self,env): 
        self._on_event_new_tick(env) 


    def __repr__(self):
        return f"name: {self._name}"\
                + f" address: {self._address}"\
                + f" network: {self._network}"\
                + f" aid: {self._aid}"\
                + f" type: {self.__class__.__name__}"
        