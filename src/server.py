import logging
import threading
import socketserver

log = logging.getLogger(__name__)


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        log.info("Connection from %s", self.client_address)
        while True:
            data = self.request.recv(1024)

            if not data:
                break

            log.debug("Received data: %s", data)
            self.request.send(data)


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
