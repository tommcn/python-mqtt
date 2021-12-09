from enum import Enum


class MQTTControlPacketType(Enum):
    CONNECT = 1
    CONNACK = 2
    PUBLISH = 3
    PUBACK = 4
    PUBREC = 5
    PUBREL = 6
    PUBCOMP = 7
    SUBSCRIBE = 8
    SUBACK = 9
    UNSUBSCRIBE = 10
    UNSUBACK = 11
    PINGREQ = 12
    PINGRESP = 13
    DISCONNECT = 14
    AUTH = 15


class MQTTControlPacketFlags(Enum):
    QOS_0 = 0x00
    RETAIN = 0x01
    QOS_1 = 0x02
    QOS_2 = 0x04
    DUP = 0x08


class MQTTConnectReasonCode(Enum):
    """
    Reason codes for the CONNACK packet
    Not an exhaustive list
    Ref: https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901079
    """

    SUCCESS = 0x00
    UNSPECIFIEDERROR = 0x80
    MALFORMEDPACKET = 0x81
    PROTOCOLERROR = 0x82
    IMPLEMENTATIONSPECIFICERROR = 0x83
    UNSUPPORTEDPROTOCOLVERSION = 0x84
