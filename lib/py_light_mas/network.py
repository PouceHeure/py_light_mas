from .message import Message, Signal


class Network:
    """
    Create a fake network. All networks are connected to gather.
    An agent of the network A can send a message to an another agent in the network B
    """

    GOBAL_NETWORK = {}

    def __init__(self, domain):
        self._domain = domain
        self._number_connections = 0
        self._address_agents = {}

        Network.GOBAL_NETWORK[domain] = self

    @classmethod
    def GET_AGENT(cls, address):
        """get agent instance from address

        Args:
            address (string): address (domain/address)

        Returns:
            Agent: instance agent connected to the network with this address
        """
        domain, _ = cls._DESERIALIZE_ADDRESS(address)
        network = cls.GOBAL_NETWORK[domain]
        if(address in network._address_agents):
            return network._address_agents[address]
        return None

    def get_name(self):
        return self._domain

    def _generator_address(self, id_connection):
        """generate an address from id_connection

        Args:
            id_connection (int): id_connection (uniq value)

        Returns:
            string: address (without domain)
        """
        return f"192.168.{id_connection//256}.{id_connection%256}"

    @classmethod
    def _SERIALIZE_ADDRESS(cls, domain, address):
        """concat domain and address

        Args:
            domain (string): the current network 
            address (string): the address 

        Returns:
            string: "domain/address"
        """
        return f"{domain}/{address}"

    @classmethod
    def _DESERIALIZE_ADDRESS(cls, address_str):
        """deserialize information in address

        Args:
            address_str (string): address with domain

        Returns:
            string,string: domain,address
        """
        address_split = address_str.split("/")
        domain = address_split[0]
        address = address_split[1]
        return domain, address

    def _allocate_address(self, address, agent):
        """try allocate the address.

        Args:
            address (string): address with domain
            agent (Agent): agent attached with this address

        Returns:
            bool: status (True= allocated)
        """
        if(not address is self._address_agents):
            self._address_agents[address] = agent
            return True
        return False

    def register_agent(self, agent):
        """register an agent to the current network
        From generation address to the allocation address

        Args:
            agent (Agent): agent to register

        Returns:
            string: agent address
        """
        id_connection = self._number_connections
        address = self._generator_address(id_connection)
        domain_address = Network._SERIALIZE_ADDRESS(self._domain, address)
        if(self._allocate_address(domain_address, agent)):
            self._number_connections += 1
            return domain_address
        return None

    def send_message(self, message):
        """send message given 
        Method called by agent for sending message to another agent

        Args:
            message (Message): message sent
        """
        get_to_agent_address = message.agent_to
        get_to_agent = Network.GET_AGENT(get_to_agent_address)
        if(get_to_agent is None):
            print(
                f"No one agent is registered with this address: {get_to_agent_address}")
        else:
            get_to_agent.event_new_message(message)

    def send_signal(self, signal):
        """send signal given

        Args:
            signal (Signal): signal sent
        """
        get_to_agent_address = signal.agent_to
        get_to_agent = Network.GET_AGENT(get_to_agent_address)
        if(get_to_agent is None):
            print(
                f"No one agent is registered with this address: {get_to_agent_address}")
        else:
            get_to_agent.event_new_signal(signal)

    def broadcast_message(self, sender, content):
        """broadcast message to all agents (in the current network)

        Args:
            sender (Agent): agent sender
            content (string): content of the message
        """
        for address, agent in self._address_agents.items():
            if(agent != sender):
                m = Message(sender=sender.get_address(),
                            dest=address, content=content)
                self.send_message(m)

    def __repr__(self):
        return f"://{self._domain}"
