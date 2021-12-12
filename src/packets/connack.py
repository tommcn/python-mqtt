import constants as c
from packet import MQTTFixedHeader, MQTTPacket, MQTTPayload, MQTTVariableHeader


class ConnackVariableHeader(MQTTVariableHeader):
    def __init__(self, connectReason):
        self.returnCode = connectReason

    def toBytes(self):
        sessionPresent = False
        out = bytearray()
        out.append(sessionPresent << 7)
        out.append(self.returnCode)
        out.append(0)
        return out


class ConnackPayload(MQTTPayload):
    def __init__(self):
        self.data = bytearray()

    def toBytes(self):
        return self.data


class ConnackPacket(MQTTPacket):
    def __init__(self, variableHeader=None, payload=None):
        header = MQTTFixedHeader(c.MQTTControlPacketType.CONNACK, 0x00)
        super().__init__(header)
        self.variableHeader = variableHeader
        self.payload = payload

    def build(self):
        variableHeader = ConnackVariableHeader(0x00)
        payload = ConnackPayload()
        packet = ConnackPacket(variableHeader, payload)
        return packet
