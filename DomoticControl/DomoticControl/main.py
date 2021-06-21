#!/usr/bin/python3

import sys
import asyncio
from time import sleep
import datahandler
import yaml
from pluginManager.manager import PluginManager
from module_observer import ModuleObserver
import data.db as db
import plugins.water_level.plugin as pl
from sqlalchemy import text

TEST = False

class DomoticControl(object):
    def __init__(self, settings: str):
        with open(settings["DC_INFO_PATH"], 'r') as f:
            self.info = yaml.load(f, Loader=yaml.SafeLoader)
        self.settings = settings
        #sleep(10) #allow postgre to start up
        print(self.settings)
        self.db = db.DCDatabase(self.settings["URI"])
        self.observer = ModuleObserver()
        self.plugins = PluginManager(self)
        self.plugins.init_plugins(self.settings["PLUGINS"])


class DomoticProtocol(asyncio.Protocol):
    def __init__(self, dc: DomoticControl):
        self.dc = dc
        self.packet_handler = datahandler.DataHandler(dc)
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        print([hex(c) for c in data])
        if TEST == True:
            if data.startswith(b"shutdownowplzuwu"):
                exit(0)
        resp = self.packet_handler.handle(bytearray(data))
        
        
        if resp is not None:
            print(resp)
            self.transport.write(resp.serialize())
    
async def main(settings_path: str):
    with open(settings_path, 'r') as f:
        settings = yaml.load(f, Loader=yaml.SafeLoader)

    control = DomoticControl(settings)

    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: DomoticProtocol(control),
        settings['HOST'], settings['PORT'])

    await server.serve_forever()

def test(settings_path):
    with open(settings_path, 'r') as f:
        settings = yaml.load(f, Loader=yaml.SafeLoader)
    import test
    sleep(0.1)
    try:
        test.tester(settings["HOST"], settings["PORT"]).test()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    if TEST:
        from threading import Thread #threading used for testing
        Thread(target = test, args=("./data/settings.yaml",)).start()       

    groups = asyncio.gather(main("./data/settings.yaml"))
    loop.run_until_complete(groups)
