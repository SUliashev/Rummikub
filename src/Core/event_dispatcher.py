class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def dispatch(self, event_type, **kwargs):
        for callback in self.listeners.get(event_type, []):
            callback(**kwargs)