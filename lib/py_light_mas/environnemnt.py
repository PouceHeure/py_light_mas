
class Environnemnt:
    """abstract class
    """

    def on_event_new_tick(self):
        """method trigged when the simulation passed a new tick
        """

    def on_event_show(self):
        """method trigged when the simulation ask to show the current state of the env
        """

    def event_new_tick(self):
        self.on_event_new_tick()

    def event_show(self):
        self.on_event_show()
