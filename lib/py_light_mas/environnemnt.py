class Environnemnt: 

    def on_event_new_tick(self):
        pass 

    def on_event_show(self):
        pass 

    def event_new_tick(self):
        self.on_event_new_tick()

    def event_show(self):
        self.on_event_show() 
