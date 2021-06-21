from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey, create_engine, UniqueConstraint
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data.base_db import BaseDB

class DCDatabase(BaseDB):
    Base = declarative_base()

    def __init__(self, uri):
        super().__init__(uri)

        select = [self.Device, self.Component]
        update = [self.Device.name]
        self.load_perms(select=select, update=update)
 
    class Device(Base):
        __tablename__ = 'device'
        _table_args__ = (UniqueConstraint('uuid', name='_uuid_uc'),)
        id = Column(Integer, primary_key = True, autoincrement=True)
        uuid = Column(BigInteger, unique = True)
        protocol_version = Column(Integer, nullable = False)
        name = Column(String, unique = True)

    class Component(Base):
        __tablename__ = 'component'
        _table_args__ = (UniqueConstraint('device_id', 'component_type', name='_device_component_uc'),)
        component_type = Column(Integer, nullable = False, primary_key = True)
        device_id = Column(Integer, ForeignKey("device.id"), primary_key = True)

    API_SELECT = [Device, Component]
    API_UPDATE = [Device.name]

    @property
    def session(self):
        return self._session

    def device_id_by_uuid(self, uuid: int, session = None):
        s = session or self._session()
        device_id = s.query(self.Device.id).filter(self.Device.uuid == uuid)
        if session is None:
            s.close()
        return device_id