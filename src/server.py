import logging
import socketserver

import constants as consts
from exceptions import MalformedPacketError

log = logging.getLogger(__name__)


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

            if (
                consts.MQTTControlPacketType(MQTTFixedHeaderType)
                == consts.MQTTControlPacketType.CONNECT
            ):
                MQTTRemaingLength = data[1]
                remaining = self.request.recv(MQTTRemaingLength)
                protocolName = remaining[:6]
                if protocolName == b"\x00\x04MQTT":
                    log.debug("Correct protocol name")
                    protocolVersion = remaining[6]
                    log.debug("Protocol version: %s", protocolVersion)
                    if (
                        protocolVersion == 0x04 or protocolVersion == 0x05
                    ):  # So uhhh... idk why but different client send me 04 or 05
                        log.debug("Supported protocol version")
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
                        clientIdentifier = str(
                            payload[1 : clientIdentifierLength + 1], encoding="UTF-8"
                        )
                        log.info("Client identifier: %s", clientIdentifier)
                        # probably need to adjust for more payload fields
                        if len(payload) == clientIdentifierLength + 1:
                            log.debug("Payload ended")
                            # here we send CONNACK

            # self.request.send(data)


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
