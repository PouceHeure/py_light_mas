import abc
import copy


class Agent:
    """Abstract class
    """

    COUNTER = 0
    SIMULATION = None

    def __init__(self, name=""):
        self._name = name
        self._address = None
        self._network = None

        self._aid = Agent.COUNTER
        Agent.COUNTER += 1

        if(Agent.SIMULATION != None):
            Agent.SIMULATION.add_agent(self)

    def get_aid(self):
        """get the aid (uniq value) agent.

        Returns:
            int: aid agent
        """
        return self._aid

    def get_address(self):
        """get the address agent

        Returns:
            string: address
        """
        return self._address

    def _guard_network(self, method_name):
        if(self._network is None):
            print(f"can't use {method_name} without connection")
            return False
        return True

    def connect(self, network):
        """connect the agent to the network given in parameter

        Args:
            network (Network): the network

        Returns:
            string: address of the agent in the network
        """
        address = network.register_agent(self)
        if(not address is None):
            self._network = network
            self._address = address
            print(f"[{self}] success connection to: {network.get_name()}")
        else:
            print(f"fail to connect: {network.get_name()}")

        return self._address

    def send_message(self, message):
        """send the message accross the network

        Args:
            message (Message): gathering sender, dest and content
        """
        if(not self._guard_network("send_message")):
            return
        self._network.send_message(message)

    def reply_message(self, message, content):
        """reply the message given with the content

        Args:
            message (Message): message received
            content (string): content in the answer
        """
        if(not self._guard_network("reply_message")):
            return
        message_reply = copy.copy(message)
        message_reply.content = content
        message_reply.agent_to = message_reply.agent_from
        message_reply.agent_from = self._address
        self.send_message(message_reply)

    @abc.abstractmethod
    def on_event_new_message(self, message):
        """method tigged when the agent received a new message

        Args:
            message (Message): message received
        """

    @abc.abstractmethod
    def on_event_new_signal(self, signal):
        """method tigged when the agent received a new signal

        Args:
            signal (Signal): signal received]
        """

    @abc.abstractmethod
    def on_event_new_tick(self, env):
        """method tigged at each new simulation tick

        Args:
            env (Environnemnt): current environnemnt where evolve the simulation
        """

    def event_new_message(self, message):
        self.on_event_new_message(message)

    def event_new_signal(self, signal):
        self.on_event_new_signal(signal)

    def event_new_tick(self, env):
        self.on_event_new_tick(env)

    def __repr__(self):
        return f"name: {self._name}"\
            + f" address: {self._address}"\
            + f" network: {self._network}"\
            + f" aid: {self._aid}"\
            + f" type: {self.__class__.__name__}"
