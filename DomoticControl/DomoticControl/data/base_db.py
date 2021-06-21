"""base database file for domoticcontrol and plugins

Adds a number of functions to manage database permissions
"""
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import table
from itertools import chain
from sqlalchemy import text

class BaseDB(object):
    
    API_SELECT = []
    API_UPDATE = []

    def __init__(self, uri):
        self.uri = uri
        self.engine = create_engine(uri)
        self._session = sessionmaker(bind=self.engine)
        self.Base.metadata.create_all(self.engine)

    def load_perms(self, select=[], update=[]):
        # print("select")
        # for row in select:
        #     if isinstance(row, DeclarativeMeta):
        #         print(row.__tablename__)
        #     else:
        #         print(dir(row))

        update_gen = (self._load_queries('UPDATE', "api_perms", update))
        select_gen = (self._load_queries('SELECT', "api_perms", select))

        for command in chain(update_gen, select_gen):
            cmd = text(command)
            print(command)
            self.engine.execute(cmd)

        # for row in update:
        #     if isinstance(row, DeclarativeMeta):
        #         print(row.__tablename__)
        #     elif isinstance(row, InstrumentedAttribute):
        #         column_name = row.key
        #         table_name = row.property.parent.class_.__tablename__
        #         print(f"{table_name}.{column_name}")

    def _load_queries(self, cmd, usr, arr):
        for row in arr:
            if isinstance(row, DeclarativeMeta):
                name = row.__tablename__
                line = f"GRANT {cmd} ON {name} TO {usr};"
            elif isinstance(row, InstrumentedAttribute):
                column = row.key
                table = row.property.parent.class_.__tablename__
                line = f"GRANT {cmd} ({column}) ON {table} TO {usr};"
            yield line