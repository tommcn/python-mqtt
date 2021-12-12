import logging

from packets.publish import PublishPacket
from packets.connack import ConnackPacket
from packets.pingresp import PingrespPacket
from packets.suback import SubackPacket

log = logging.getLogger(__name__)


class ClientConnection:
    def __init__(self, request, clientIdentifier):
        self.request = request
        self.clientIdentifier = clientIdentifier

    def CONNACK(self):
        log.info("Sending CONNACK")
        p = ConnackPacket().build().toBytes()
        self.request.send(p)

    def PINGRESP(self):
        log.info("Sending PINGRESP")
        self.request.send(PingrespPacket().build().toBytes())

    def SUBACK(self, packetIdentifier, reasonCode):
        log.info("Sending SUBACK")
        p = SubackPacket().build(packetIdentifier, reasonCode).toBytes()
        self.request.send(p)

    def PUBLISH(self, topic, payload, packetIdentifier):
        log.info("Sending PUBLISH with payload: %s", payload)
        p = PublishPacket().build(topic, payload, packetIdentifier).toBytes()
        self.request.send(p)
