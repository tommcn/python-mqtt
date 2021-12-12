import logging

from packet import CONNACK, PINGRESP, SUBACK
from packets.publish import PublishPacket

log = logging.getLogger(__name__)


class ClientConnection:
    def __init__(self, request, clientIdentifier):
        self.request = request
        self.clientIdentifier = clientIdentifier

    def CONNACK(self, reasonCode):
        log.info("Sending CONNACK")
        self.request.send(CONNACK(0x00, reasonCode).asBytes())

    def PINGRESP(self):
        log.info("Sending PINGRESP")
        self.request.send(PINGRESP().asBytes())

    def SUBACK(self, packetIdentifier, reasonCode):
        log.info("Sending SUBACK")
        self.request.send(SUBACK(packetIdentifier, reasonCode).asBytes())

    def PUBLISH(self, topic, payload, packetIdentifier):
        log.info("Sending PUBLISH with payload: %s", payload)
        p = PublishPacket().build(topic, payload, packetIdentifier).toBytes()
        print(list(p))
        self.request.send(p)
