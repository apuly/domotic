#this plugin has been realised to deal with the data received from water level sensors

from pluginManager import base_plugin
from data.component_types import ComponentTypes
from data.events import SubscribableEventTypes as Events

from main import DomoticProtocol
from datetime import datetime

from . import db_schema


class GroundWaterPlugin(base_plugin.DomoticPlugin):
    def __init__(self, dc: DomoticProtocol):
        super().__init__(dc)
        dc.observer.subscribe(Events.SendValue, ComponentTypes.GroundWaterSensor, self.on_module_receive)
        try:
            self._db = db_schema.DBSchema(dc.db.uri) #it breaks here
        except Exception as e:
            print(e)
        
    def on_module_receive(self, data):
        now = datetime.now()
        sensor_value = int.from_bytes(data['raw_data'][:2], 'big')
        id = self._dc.db.device_id_by_uuid(data["uuid"]).scalar_subquery()
        session = self._db.session()
        entry = self._db.GroundWater(time = now, value = sensor_value, module_id = id)
        session.add(entry)
        session.commit()
        session.close()

        


