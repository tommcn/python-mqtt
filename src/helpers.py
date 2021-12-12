from struct import pack


def intToBytes(val, length) -> bytes:
    if length == 1:
        fmt = "!B"
    elif length == 2:
        fmt = "!H"
    return pack(fmt, val)


def encodeUTF8String(string):
    data = string.encode("utf-8")
    dataLength = len(data)
    return pack("!H", dataLength) + data
