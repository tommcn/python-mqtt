import constants as c
from helpers import intToBytes
from packet import MQTTFixedHeader, MQTTPacket, MQTTPayload, MQTTVariableHeader


class SubackVariableHeader(MQTTVariableHeader):
    def __init__(self, packetIdentifier):
        self.packetIdentifier = packetIdentifier

    def toBytes(self):
        out = bytearray()
        out.extend(intToBytes(self.packetIdentifier, 2))
        out.extend((0,))
        return out


class SubackPayload(MQTTPayload):
    def __init__(self, reasonCode):
        self.reasonCode = reasonCode

    def toBytes(self):
        return bytearray((self.reasonCode,))


class SubackPacket(MQTTPacket):
    def __init__(self, variableHeader=None, payload=None):
        header = MQTTFixedHeader(c.MQTTControlPacketType.SUBACK, 0x00)
        super().__init__(header)
        self.variableHeader = variableHeader
        self.payload = payload

    def build(self, packetIdentifier, reasonCode):
        variableHeader = SubackVariableHeader(packetIdentifier)
        payload = SubackPayload(reasonCode)
        packet = SubackPacket(variableHeader=variableHeader, payload=payload)
        return packet
