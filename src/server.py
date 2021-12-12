import logging
import socketserver
import threading
import uuid

import constants as consts
from connection import ClientConnection
from exceptions import (ImplementationSpecificError, MalformedPacketError,
                        ProtocolError)

log = logging.getLogger(__name__)

lock = threading.Lock()
connections = {}  # Shhh


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        log.info("Connection from %s", self.client_address)
        while True:
            # Expecting 2 byte MQTT Control Packet
            data = self.request.recv(2)

            if not data:
                break

            log.debug("Received data: %s", data)

            byte = data[0]
            MQTTFixedHeaderType = byte >> 4
            MQTTFixedHeaderFlags = byte & 0x0F
            log.debug(
                "MQTT Fixed Header Type: %s (%s)",
                MQTTFixedHeaderType,
                consts.MQTTControlPacketType(MQTTFixedHeaderType),
            )
            log.debug("MQTT Fixed Header Flags: %s", MQTTFixedHeaderFlags)

            match consts.MQTTControlPacketType(MQTTFixedHeaderType):
                case consts.MQTTControlPacketType.CONNECT:
                    self.handle_CONNECT(data)

                case consts.MQTTControlPacketType.PINGREQ:
                    self.handle_PINGREQ()

                case consts.MQTTControlPacketType.SUBSCRIBE:
                    self.handle_SUBSCRIBE(data)

                case consts.MQTTControlPacketType.DISCONNECT:
                    log.info("Received DISCONNECT")
                    break

                case _:
                    raise ImplementationSpecificError(f"Non implemented packet type: {consts.MQTTControlPacketType(MQTTFixedHeaderType)}")

    def handle_CONNECT(self, data):
        MQTTRemaingLength = data[1]
        remaining = self.request.recv(MQTTRemaingLength)
        protocolName = remaining[:6]

        if protocolName == b"\x00\x04MQTT":
            log.debug("Correct protocol name")
        else:
            log.error("Incorrect protocol name")
            raise ProtocolError(f"Incorrect protocol name provided: {protocolName}")

        protocolVersion = remaining[6]
        log.debug("Protocol version: %s", protocolVersion)
        if (
            protocolVersion == 0x04 or protocolVersion == 0x05
        ):  # So uhhh... idk why but different client send me 04 or 05
            log.debug("Supported protocol version")
        else:
            log.error("Unsupported protocol version")
            raise ProtocolError(f"Unsupported protocol version: {protocolVersion}")

        connectFlags = remaining[7]
        log.debug("Connect flags: %s", connectFlags)
        if (connectFlags & 0x01) == 0x01:
            log.error("Reserved bit set")
            raise MalformedPacketError(
                f"Violation of MQTT protocol: reserved bit set in connect flags ({connectFlags})"
            )

        keepAlive = remaining[8] * 256 + remaining[9]
        log.debug("Keep alive: %ss", keepAlive)

        propertiesLength = remaining[10]
        log.debug("Properties length: %s", propertiesLength)
        properties = remaining[11 : 11 + propertiesLength]
        log.debug("Properties: %s", properties)

        payload = remaining[11 + propertiesLength :]
        log.debug("Payload: %s", payload)
        clientIdentifierLength = payload[0]
        if clientIdentifierLength == 0:
            clientIdentifier = uuid.uuid4().hex
        else:
            clientIdentifier = str(
                payload[1 : clientIdentifierLength + 1], encoding="UTF-8"
            )

        log.info("Client identifier: %s", clientIdentifier)
        self.clientIdentifier = clientIdentifier

        # probably need to adjust for more payload fields
        # And kinda wack ngl
        if (
            len(payload) == clientIdentifierLength + 1
            or len(payload) == clientIdentifierLength + 2
            or clientIdentifierLength == 0
        ):
            log.debug("Payload ended")
            conn = ClientConnection(self.request, clientIdentifier)
            with lock:
                connections[conn.clientIdentifier] = conn
            conn.CONNACK()
            # somewhere here we send a CONNACK

    def handle_PINGREQ(self):
        log.info("Received PINGREQ")
        connections[self.clientIdentifier].PINGRESP()

    def handle_SUBSCRIBE(self, data):
        log.info("Received SUBSCRIBE")
        remainingLength = data[1]
        remaining = self.request.recv(remainingLength)
        if 130 & 0x0F == 2:
            log.debug("Correct packet type")
        else:
            raise MalformedPacketError("Reserved bits set incorrectly")
        packetIdentifier = remaining[0] * 256 + remaining[1]
        log.debug("Packet identifier: %s", packetIdentifier)
        propertiesLength = remaining[2]
        log.debug("Properties length: %s", propertiesLength)
        properties = remaining[3 : 3 + propertiesLength]
        log.debug("Properties: %s", properties)
        payload = remaining[2 + propertiesLength + 1 :]
        topicLength = payload[0] * 256 + payload[1]
        topic = str(payload[1 : 2 + topicLength], encoding="UTF-8")
        log.debug("Topic: %s", topic)
        connections[self.clientIdentifier].SUBACK(packetIdentifier, 1)
        connections[self.clientIdentifier].PUBLISH("topic", "hello", packetIdentifier)


class Server(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


def runserver(host, port):
    with Server((host, port), TCPHandler) as server:
        try:
            log.info("Starting server on %s:%s", host, port)
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
            print()
            log.info("Server stopped")
