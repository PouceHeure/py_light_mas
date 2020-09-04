


class Message: 

    def __init__(self,sender="",dest="",content=None): 
        self.agent_from = sender
        self.agent_to = dest
        self.content = content 

    def __repr__(self):
        return f"from: {self.agent_from} to: {self.agent_to} content: {self.content}"