from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, create_engine, BigInteger, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from data.db import DCDatabase
from data.base_db import BaseDB


class DBSchema(BaseDB):
    Base = declarative_base()

    _session = None

    def __init__(self, uri):
        super().__init__(uri)

        Pump = self.Pump
        select = [Pump]
        update = [Pump.pump_time, Pump.groundwatersensor_id, Pump.target_groundwater_value]
        self.load_perms(select=select, update=update)

    class Pump(Base):
        __tablename__ = 'water_pump'
        time = Column(DateTime, nullable=True)
        device_id = Column(Integer, ForeignKey(DCDatabase.Device.id), nullable=False, primary_key=True )
        groundwatersensor_id = Column(Integer, nullable=True, unique=True)
        target_groundwater_value = Column(Integer, nullable=True)
        pump_time = Column(Integer, nullable=True)
        activate_pump = Column(Boolean, default=False)

    #constants to load api permissions into postgresql
    API_SELECT = [Pump]
    API_UPDATE = [Pump.pump_time, Pump.groundwatersensor_id, Pump.target_groundwater_value]

    @property
    def session(self):
        return self._session
