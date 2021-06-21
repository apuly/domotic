#basic implementation of the observer model
#used to send messages to plugins

from enum import EnumMeta
from data.component_types import ComponentTypes as Components
from data.events import SubscribableEventTypes as Events

class ModuleObserver():
    subscribers = {} #dictionary with subscribers per module type

    def subscribe(self, event_type, module_type, func):
        if isinstance(event_type, Events):
            event_type = event_type.value
        if isinstance(module_type, Components):
            module_type = module_type.value
        if event_type not in self.subscribers:
            self.subscribers[event_type] = {}
        if module_type not in self.subscribers[event_type]:
            self.subscribers[event_type][module_type] = set()
        if func in self.subscribers[event_type][module_type]:
            print("func is already subscribed to module")
        else:
            self.subscribers[event_type][module_type].add(func)
    
    def unsubscribe(self, event_type, module_type, func):
        if isinstance(event_type, Events):
            event_type = event_type.value
        if isinstance(module_type, Components):
            module_type = module_type.value
        if func in self.subscribers[event_type][module_type]:
            self.subscribers[event_type][module_type].discard(func)
            if len(self.subscribers[event_type][module_type]) == 0:
                del self.subscribers[event_type][module_type]
                if len(self.subscribers[event_type] == 0):
                    del self.subscribers[event_type]

    def send_message(self, event_type, module_type, data):
        if isinstance(event_type, Events):
            event_type = event_type.value
        if isinstance(module_type, Components):
            module_type = module_type.value
        
        if event_type in self.subscribers \
            and module_type in self.subscribers[event_type]:

            functions = self.subscribers[event_type][module_type]
            returned_values = [func(data) for func in functions]
            filtered_returns = [val for val in returned_values if val is not None]
            if len(filtered_returns) == 1:
                return filtered_returns[0]
            elif len(filtered_returns) > 1:
                print("Error: multiple plugins returning values, only one allowed")
            return None
            
        else:
            print(f"Call to {event_type}:{module_type} made, but no subscribers")
            return None