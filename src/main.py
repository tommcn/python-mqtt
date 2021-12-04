import argparse

from server import runserver

parser = argparse.ArgumentParser(description="MQTT server")

parser.add_argument("-p", "--port", type=int, default=1883, help="Port to listen on")
parser.add_argument(
    "-H", "--host", type=str, default="localhost", help="Host to bind to"
)


def main():
    args = parser.parse_args()
    runserver(args.host, args.port)


if __name__ == "__main__":
    main()
