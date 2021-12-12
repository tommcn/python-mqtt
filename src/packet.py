import constants as c


class MQTTFixedHeader:
    def __init__(self, packetType: c.MQTTControlPacketType, length=0) -> None:
        self.packetType = packetType
        self.remainingLength = length
        self.flags = 0

    def toBytes(self):
        # Adapted from: https://github.dev/beerfactory/hbmqtt/blob/07c4c70f061003f208ad7e510b6e8fce4d7b3a6c/hbmqtt/mqtt/packet.py#L41-L52
        def encodeRemainingLength(length: int):
            encoded = bytearray()
            while True:
                length_byte = length % 0x80
                length //= 0x80
                if length > 0:
                    length_byte |= 0x80
                encoded.append(length_byte)
                if length <= 0:
                    break
            return encoded

        out = bytearray()
        out.append(self.packetType.value << 4)
        out.extend(encodeRemainingLength(self.remainingLength))

        return out


class MQTTVariableHeader:
    def toBytes(self):
        pass


class MQTTPayload:
    def toBytes(self):
        pass


class MQTTPacket:
    def __init__(
        self,
        fixedHeader,
        variableHeader=None,
        payload=None,
    ) -> None:
        self.fixedHeader = fixedHeader
        self.variableHeader = variableHeader
        self.payload = payload

    def toBytes(self) -> bytes:
        if self.variableHeader:
            variableHeaderBytes = self.variableHeader.toBytes()
        else:
            variableHeaderBytes = b""

        if self.payload:
            payloadBytes = self.payload.toBytes()
        else:
            payloadBytes = b""

        self.fixedHeader.remainingLength = len(variableHeaderBytes) + len(payloadBytes)
        fixedHeaderBytes = self.fixedHeader.toBytes()

        return fixedHeaderBytes + variableHeaderBytes + payloadBytes


class CONNECT(MQTTPacket):
    def verify(self, data):
        return True

    def handle(self, data):
        return super().handle(data)


# class SUBACK(MQTTPacket):
#     def __init__(self, packetIdentifier, returnCode):
#         self.packetIdentifier = packetIdentifier
#         self.returnCode = returnCode

#     def asBytes(self):
#         packetType = c.MQTTControlPacketType.SUBACK
#         firstbyte = packetType.value << 4
#         remainingLength = None
#         packetIdentifier = self.packetIdentifier
#         propertiesLength = 0
#         reason = self.returnCode  # 0x00 for QoS 0
#         remainingLength = (
#             len(packetIdentifier.to_bytes(2, "big"))
#             + len(reason.to_bytes(1, "big"))
#             + len(propertiesLength.to_bytes(1, "big"))
#         )
#         return bytearray(
#             (
#                 firstbyte,
#                 remainingLength,
#                 packetIdentifier.to_bytes(2, "big")[0],
#                 packetIdentifier.to_bytes(2, "big")[1],
#                 propertiesLength,
#                 reason,
#             )
#         )
