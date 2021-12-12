import constants as c
from packet import MQTTFixedHeader, MQTTPacket


class PingrespPacket(MQTTPacket):
    def __init__(self):
        header = MQTTFixedHeader(c.MQTTControlPacketType.PINGRESP, 0x00)
        super().__init__(header)

    def build(self):
        packet = PingrespPacket()
        return packet
