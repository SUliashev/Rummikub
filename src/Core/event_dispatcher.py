from typing import Callable, Any

class EventDispatcher:
    listeners: dict[str, Callable[..., Any]]

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type: str, callback: Callable[..., Any]) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def dispatch(self, event_type: str, **kwargs: Callable[..., Any]) -> None:
        for callback in self.listeners.get(event_type, []):
            callback(**kwargs)