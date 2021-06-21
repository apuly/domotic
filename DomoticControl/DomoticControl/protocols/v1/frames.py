"""
Module written for simplifying unpacking of packets received by the DC

FrameParser.parse is called with the executed command, the length of the command and the
rest of the raw data.

The raw data is further unpacked based on the structures dictionary near the bottom
of the module

The result is a dictionary with the keys and data as defined in the structure
"""
from . import domoticcom

REST = 0

class FrameParser():
    @staticmethod
    def parse(command, length, data):
        #protocol version and length have already been handled.
        #length is passed anyways for the sake of validation
        structure_array = structures[command]
        out = {"command": command, "protocol": 1}
        data_position = 0 #tracks the current position in the data frame

        for entry in structure_array:
            if entry.length == REST:
                
                if data_position <= length: #if there's still data left in the buffer or end of buffer is reached
                    data_target = data[data_position:]
                    data_position += len(data_target)
                    out[entry.name] = entry.parse(data_target)
                    break #rest is always the last in the series (or if it isn't your frame structure is wrong)
                          #so function breaks after getting to rest
                else:
                    print(data_position, length)
                    print(structure_array)
                    raise FrameLengthMismatch()
            else:
                data_target = data[data_position:data_position+entry.length]
                out[entry.name] = entry.parse(data_target)
                data_position += entry.length
               

        if data_position != length:
            print(data_position, length)
            raise FrameLengthMismatch()
        
        return out

        
class StructureEntry():
    def __init__(self, name, length, parser_func):
        self._name = name
        self._length = length
        self._func = parser_func

    @property
    def name(self):
        return self._name

    def parse(self, data):
        return self._func(data)
    
    @property
    def length(self):
        return self._length

int_parser = lambda data: int.from_bytes(data, 'big')
unparsed = lambda data: data
string_parser = lambda data: data.decode('utf-8')

structures = {
    domoticcom.to_dc.REQUEST_ID: [
    ],

    domoticcom.to_dc.REQUEST_INFO: [
    ],

    domoticcom.to_dc.MODULE_INFO: [
        StructureEntry("uuid", domoticcom.UUID_SIZE, int_parser),
        StructureEntry("component_type", domoticcom.DEVICE_TYPE_SIZE, int_parser)
    ],

    domoticcom.to_dc.SEND_VALUE: [
        StructureEntry("uuid", domoticcom.UUID_SIZE, int_parser),
        StructureEntry("component_type", domoticcom.DEVICE_TYPE_SIZE, int_parser),
        StructureEntry("raw_data", REST, unparsed)
    ],
    
    domoticcom.to_dc.REQUEST_VALUE: [
        StructureEntry("uuid", domoticcom.UUID_SIZE, int_parser),
        StructureEntry("component_type", domoticcom.DEVICE_TYPE_SIZE, int_parser),
        StructureEntry("raw_data", REST, unparsed)
    ]
}

class FrameLengthMismatch(Exception):
    pass