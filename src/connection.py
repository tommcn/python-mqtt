import logging

from packet import CONNACK

log = logging.getLogger(__name__)


class ClientConnection:
    def __init__(self, request, clientIdentifier):
        self.request = request
        self.clientIdentifier = clientIdentifier

    def CONNACK(self, reasonCode):
        log.info("Sending CONNACK")
        self.request.send(CONNACK(0x00, reasonCode).asBytes())
