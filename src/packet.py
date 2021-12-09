import constants as c


class MQTTPacket:
    def handle(self, data):
        raise NotImplementedError

    def verify(self, data):
        raise NotImplementedError


class CONNECT(MQTTPacket):
    def verify(self, data):
        return True

    def handle(self, data):
        return super().handle(data)


class CONNACK(MQTTPacket):
    def __init__(self, connectAcknowledgeFlags, connectReasonCode):
        self.connectAcknowledgeFlags = connectAcknowledgeFlags
        self.connectReasonCode = connectReasonCode

    def asBytes(self):
        packetType = c.MQTTControlPacketType.CONNACK
        firstbyte = packetType.value << 4
        remainingLength = None  # Cause we don't know the length yet
        sessionPresent = False << 7  # We're assuming a clean session for now
        connectReasonCode = self.connectReasonCode.value
        properties = 0  # No properties for now :)
        # Assigned Client Identifier
        remainingLength = (
            len(sessionPresent.to_bytes(1, "big"))
            + len(connectReasonCode.to_bytes(1, "big"))
            + len(properties.to_bytes(1, "big"))
        )
        print(remainingLength)
        print(sessionPresent.to_bytes(1, "big"))
        print(
            (firstbyte, remainingLength, sessionPresent, connectReasonCode, properties)
        )
        return bytearray(
            (firstbyte, remainingLength, sessionPresent, connectReasonCode, properties)
        )
