import logging
import socketserver

log = logging.getLogger(__name__)


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        log.info("Connection from %s", self.client_address)
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            self.request.send(data)


class Server(socketserver.TCPServer):
    pass


def runserver(host, port):
    with Server((host, port), TCPHandler) as server:
        try:
            log.info("Starting server on %s:%s", host, port)
            server.serve_forever()
        except KeyboardInterrupt:
            print()
            log.info("Server stopped")
