from plugins.water_level.plugin import GroundWaterPlugin
from sqlalchemy.sql.expression import null
from data.component_types import ComponentTypes
from pluginManager import base_plugin
from main import DomoticProtocol
from data.component_types import ComponentTypes
from data.events import SubscribableEventTypes as Events
from protocols.v1.packets import respond_value
from sqlalchemy.exc import IntegrityError
import  psycopg2.errors as errors
from datetime import datetime
from . import db_schema


class WaterPumpPlugin(base_plugin.DomoticPlugin):
    def __init__(self, dc: DomoticProtocol):
        super().__init__(dc)
        #dc.observer.subscribe(ComponentTypes.WaterPump, self.on_waterpump_receive)
        dc.observer.subscribe(Events.SendValue, ComponentTypes.GroundWaterSensor, self.on_waterlevel_receive)
        dc.observer.subscribe(Events.RequestValue, ComponentTypes.WaterPump, self.on_pumptime_request)
        dc.observer.subscribe(Events.ModuleInfo, ComponentTypes.WaterPump, self.on_waterpump_register)

       
        self._db = db_schema.DBSchema(dc.db.uri)
      
        
    def on_waterlevel_receive(self, data):
        Pump = self._db.Pump
        sensor_value = int.from_bytes(data['raw_data'][:2], 'big')

        s = self._db.session()
        module_id = self._dc.db.device_id_by_uuid(data['uuid']).scalar_subquery()
        pump = s.query(Pump).filter(
            Pump.groundwatersensor_id == module_id,
            Pump.target_groundwater_value is not None
        ).first()
        
        if pump is not None and pump.target_groundwater_value < sensor_value:
            pump.activate_pump = True
            s.commit()
        s.close()

    def on_waterpump_register(self, data):
        print("Loading new entry waterpump entry into database")
        Pump = self._db.Pump
        s = self._db.session()

        device_id = self._dc.db.device_id_by_uuid(data['uuid'], session=s).scalar_subquery()
        try:
            newPump = Pump(device_id=device_id)
            s.add(newPump)
            s.commit()
        except IntegrityError:
            pass
        finally:
            s.close()

    def on_pumptime_request(self, data):
        device_id = self._dc.db.device_id_by_uuid(data['uuid']).scalar_subquery()
        Pump = self._db.Pump

        s = self._db.session()
        pump = s.query(Pump).filter(Pump.device_id==device_id).first()
        if pump and pump.pump_time and pump.activate_pump:
            #return that pump should be activated
            pump_time = pump.pump_time
            pump.activate_pump = False
            s.commit()
        else:
            pump_time = 0
        s.close()

        pump_time = pump_time.to_bytes(2, 'big')
        waterpump_type = ComponentTypes.WaterPump.value.to_bytes(2, 'big')
        packet = respond_value(self._dc.info['ID'], waterpump_type, pump_time)
        return packet

        
    # def on_waterpump_receive(self, data):
    #     Pump = self._db.Pump
    #     session = self._db.session()

    #     count = session.query(Pump).filter(Pump.groundwatersensor_id == data["uuid"] and Pump.activate_pump == True).count()
    #     if count != 0:
            


        