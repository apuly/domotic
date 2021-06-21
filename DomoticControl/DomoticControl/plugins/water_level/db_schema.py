from sqlalchemy import Column, Integer, ForeignKey, DateTime, create_engine, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from data.db import DCDatabase
from data.base_db import BaseDB

class DBSchema(BaseDB):
    Base = declarative_base()

    _session = None

    def __init__(self, uri):
        super().__init__(uri)
        self.load_perms(select=[self.GroundWater])

    class GroundWater(Base):
        __tablename__ = 'groundwater'
        _table_args__ = (UniqueConstraint('device_id', 'time', name='_groundwater_device_time_uc'),)
        id = Column(Integer, primary_key=True, autoincrement=True)
        time = Column(DateTime, nullable=False)
        value = Column(Integer, nullable=False)
        module_id = Column(Integer, ForeignKey(DCDatabase.Device.id))

    @property
    def session(self):
        return self._session

