import time

#from data.db import Device, session
from lib.uuid64 import uuid64
from data.component_types import ComponentTypes
from data.events import SubscribableEventTypes as Events
from . import domoticcom, frames, packets

to_dc = domoticcom.to_dc

class protocol(object):
    def __init__(self, dc):
        self._dc = dc

    def print_id(self, id: int):
        data = id.to_bytes(8, 'big')
        s = ".".join([str(b) for b in data])
        print(s)

    def handle(self, frame_length: int, data: bytes):
        id = data[:domoticcom.CMD_ID_SIZE]
        id = int.from_bytes(id, 'big')
        del data[:domoticcom.CMD_ID_SIZE]

        try:
            command = to_dc(id)
        except ValueError:
            print(f"ID {id} requested, but command doesn't exist")
            raise NotImplementedError
        else:
            frame = frames.FrameParser.parse(command, frame_length-5, data)
            print(frame)
            return self._handle_command(command, frame)


    def _handle_command(self, command: Events, data: dict):

        handler_name = f"handle_{command.name.lower()}"  
        try:
            handler = getattr(self, handler_name)
        except AttributeError:
            print(f"{command} not implemented!")
        else: 
            return handler(data)

    def handle_request_id(self, data: dict):
        module_id = uuid64().int()
        packet = packets.send_id(module_id)
        return packet

    def handle_request_info(self, data: dict):
        packet = packets.send_info(self._dc.info['ID'])
        return packet

    def handle_module_info(self, data: dict):
        device_type = self._dc.db.Device
        component_type = self._dc.db.Component
        s = self._dc.db.session()
        uuid = data["uuid"]

        #check if uuid is already present in database
        resp = s.query(device_type).filter(device_type.uuid == uuid).count()
        if resp == 0: #if not, add uuid to database
            device = device_type(uuid = uuid, protocol_version=1)
            s.add(device)

        #check if uuid already has module type connected to it
        device_id = self._dc.db.device_id_by_uuid(data["uuid"], session=s).scalar_subquery()
        resp = s.query(component_type).filter(
            component_type.device_id == device_id,
                component_type.component_type == data["component_type"]
            ).count()
        if resp == 0: #if not, add module type
            component = component_type(component_type = data["component_type"], device_id = device_id)
            s.add(component)
        
        s.commit()
        s.close()
        self._dc.observer.send_message(Events.ModuleInfo, data["component_type"], data)

    def handle_send_value(self, data: dict):
        component = self._dc.db.Component
        
        s = self._dc.db.session()
        device_id = self._dc.db.device_id_by_uuid(data["uuid"], session=s).scalar_subquery()
        resp = s.query(component).filter(component.device_id == device_id).count()
        s.close()
        device_id = self._dc.db.device_id_by_uuid(data['uuid'])

        if resp == 0:
            print(f"{resp} is not a component of module {data['uuid']}")
        try:
            component_type = ComponentTypes(data["component_type"])
        except ValueError:
            print(f"{data['component_type']} not a valid component ID")
            return
        data["type"] = component_type
        self._dc.observer.send_message(Events.SendValue, component_type, data)

    def handle_request_value(self, data: dict):
        component = self._dc.db.Component
        
        s = self._dc.db.session()
        device_id = self._dc.db.device_id_by_uuid(data["uuid"], session=s).scalar_subquery()
        resp = s.query(component).filter(component.device_id == device_id).count()
        s.close()
        
        if resp == 0:
            print(f"{resp} is not a component of module {data['uuid']}")
        try:
            component_type = ComponentTypes(data["component_type"])
        except ValueError:
            print(f"{data['component_type']} not a valid component ID")
            return
        data["type"] = component_type
        return self._dc.observer.send_message(Events.RequestValue, component_type, data)

