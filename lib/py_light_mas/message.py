

class Signal:

    V_STOP = 0
    V_END_TASK = 1

    def __init__(self, sender="", dest="", value=None):
        self.agent_from = sender
        self.agent_to = dest
        self.value = value


class Message:

    def __init__(self, sender="", dest="", content=None):
        self.agent_from = sender
        self.agent_to = dest
        self.content = content

    def __repr__(self):
        return f"from: {self.agent_from} to: {self.agent_to} content: {self.content}"
