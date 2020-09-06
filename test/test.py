import unittest

from py_light_mas.message import Signal,Message
from py_light_mas.agent import Agent
from py_light_mas.network import Network
from py_light_mas.simulation import Simulation
from py_light_mas.environnemnt import Environnemnt



class SimpleAgent(Agent):

    def __init__(self, address_teammate=None, **kargs):
        super(SimpleAgent, self).__init__(**kargs) 
        self.new_tick = False 
        self.message = None 
        self.signal = None
        self.signal_kind = False 
        self.address_teammate = address_teammate

        self.signal_sent = None
        self.message_sent = None
        self.connect_slot(Signal.V_BEGIN,self.on_event_special_signal)

    def on_event_new_tick(self, env):
        self.new_tick = True 
        if(self.address_teammate != None): 
            self.message_sent = Message(sender=self._address,dest=self.address_teammate,content="test")
            self.send_message(self.message_sent)
            self.signal_sent = Signal(sender=self._address,dest=self.address_teammate,kind=Signal.V_BEGIN)
            self.send_signal(self.signal_sent)

    def on_event_new_message(self, message):
        self.message = message 

    def on_event_special_signal(self): 
        self.signal_kind = True

    def on_event_new_signal(self, signal):
        self.signal = signal 


class SimpleEnvironnment(Environnemnt):

    def __init__(self,**kargs): 
        super(SimpleEnvironnment, self).__init__(**kargs) 
    


class SimpleSimulation(Simulation):
    def __init__(self,**kargs): 
        super(SimpleSimulation, self).__init__(**kargs) 
        netA = Network("netA")
        netB = Network("netB")

        self.agentA1 = SimpleAgent(name="agentA1")
        address_A1 = self.agentA1.connect(netA)

        self.agentA2 = SimpleAgent(name="agentA2",address_teammate=address_A1)
        address_A2 = self.agentA2.connect(netB)


class TestCaseAgent(unittest.TestCase):

    def setUp(self):
        self.sim = SimpleSimulation()
        self.sim.run()

    def test_new_tick(self):
        self.assertTrue(self.sim.agentA1.new_tick)

    def test_message_no_none(self):
        initial_message = self.sim.agentA2.message_sent
        self.assertIsNotNone(initial_message)
       
    def test_messages_equals(self):
        initial_message = self.sim.agentA2.message_sent
        final_message = self.sim.agentA1.message
        self.assertEqual(initial_message, final_message)

    def test_signal_no_none(self):
        initial_signal = self.sim.agentA2.signal_sent
        self.assertIsNotNone(initial_signal)

    def test_singals_equals(self):
        initial_signal = self.sim.agentA2.signal_sent
        final_signal = self.sim.agentA1.signal
        self.assertEqual(initial_signal, final_signal)

    def test_signal_special(self):
        self.assertTrue(self.sim.agentA1.signal_kind)


if __name__ == '__main__':
    unittest.main()