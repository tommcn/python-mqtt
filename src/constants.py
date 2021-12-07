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
