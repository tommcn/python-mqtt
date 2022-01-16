# Ladybug

A watered-down vanilla python implementation of the MQTTv5 protocol. The standard can be found [here](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html).

## Usage

```shell
$ cd src

$ python3 main.py -h
usage: main.py [-h] [-p PORT] [-H HOST]

MQTT server

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to listen on
  -H HOST, --host HOST  Host to bind to

$ python3 main.py
[INFO] Starting server on localhost:1883
```

## Features

- Publishing messages to an arbitrary topic
- Subscribing to any number of topics and receiving messages

## Caveats

- Only QoS 0 is supported.
- Authentication is not supported.

## Requirements

Python 3.10.0 or later
