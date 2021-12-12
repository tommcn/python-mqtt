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


# class CONNACK(MQTTPacket):
#     def __init__(self, connectAcknowledgeFlags, connectReasonCode):
#         self.connectAcknowledgeFlags = connectAcknowledgeFlags
#         self.connectReasonCode = connectReasonCode

#     def asBytes(self):
#         packetType = c.MQTTControlPacketType.CONNACK
#         firstbyte = packetType.value << 4
#         remainingLength = None  # Cause we don't know the length yet
#         sessionPresent = False << 7  # We're assuming a clean session for now
#         connectReasonCode = self.connectReasonCode.value
#         properties = 0  # No properties for now :)
#         # Assigned Client Identifier
#         remainingLength = (
#             len(sessionPresent.to_bytes(1, "big"))
#             + len(connectReasonCode.to_bytes(1, "big"))
#             + len(properties.to_bytes(1, "big"))
#         )
#         return bytearray(
#             (firstbyte, remainingLength, sessionPresent, connectReasonCode, properties)
#         )
