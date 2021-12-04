import socketserver


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
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
            server.serve_forever()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
