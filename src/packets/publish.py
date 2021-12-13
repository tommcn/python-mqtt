import constants as c
from helpers import encodeUTF8String, intToBytes
from packet import MQTTFixedHeader, MQTTPacket, MQTTPayload, MQTTVariableHeader


class PublishVariableHeader(MQTTVariableHeader):
    def __init__(self, topicName, packetID):
        # TODO: Check for illegal characters in topic name
        self.topicName = topicName
        self.packetID = packetID

    def toBytes(self):
        out = bytearray()
        out.extend(encodeUTF8String(self.topicName))
        # We are assuming QoS 0, so packetIdentifer is not included in packet
        # out.extend(intToBytes(self.packetID, 2))

        out.extend((0,))
        return out


class PublishPayload(MQTTPayload):
    def __init__(self, data):
        self.data = data

    def toBytes(self):
        return bytes(self.data, encoding="UTF-8")


class PublishPacket(MQTTPacket):
    def __init__(self, variableHeader=None, payload=None):
        header = MQTTFixedHeader(c.MQTTControlPacketType.PUBLISH)
        super().__init__(header)
        self.variableHeader = variableHeader
        self.payload = payload

    def build(self, topic, message, packetIdentifier):
        variableHeader = PublishVariableHeader(topic, packetIdentifier)
        payload = PublishPayload(message)
        packet = PublishPacket(variableHeader=variableHeader, payload=payload)
        return packet
