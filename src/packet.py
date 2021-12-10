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
        return bytearray(
            (firstbyte, remainingLength, sessionPresent, connectReasonCode, properties)
        )


class PINGRESP(MQTTPacket):
    def asBytes(self):
        return bytearray((c.MQTTControlPacketType.PINGRESP.value << 4, 0))


class SUBACK(MQTTPacket):
    def __init__(self, packetIdentifier, returnCode):
        self.packetIdentifier = packetIdentifier
        self.returnCode = returnCode

    def asBytes(self):
        packetType = c.MQTTControlPacketType.SUBACK
        firstbyte = packetType.value << 4
        remainingLength = None
        packetIdentifier = self.packetIdentifier + 4
        properties = 0
        propertiesLength = 0
        reason = self.returnCode  # 0x00 for QoS 0
        remainingLength = (
            len(propertiesLength.to_bytes(1, "big"))
            + len(packetIdentifier.to_bytes(2, "big"))
            + len(reason.to_bytes(1, "big"))
        )
        return bytearray(
            (
                firstbyte,
                remainingLength,
                (packetIdentifier & 0xFF),
                ((packetIdentifier >> 8) & 0xFF),
                propertiesLength,
                reason,
            )
        )
