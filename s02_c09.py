# PKCS#7 padding

def pad(message, n, method = "PKCS#7"):
    """
    handles strings or bytes, maybe that's bad practice to do in one

    :param message:
    :param n:
    :param method:
    :return:
    """
    if method == "PKCS#7":
        if n > 255:
            raise ValueError('For PKCS#7 padding, block size must be <256')
        # pad with number of bytes added
        if len(message) % n == 0:
            p = n
        else:
            p = n - (len(message) % n)

    if isinstance(message, str):
        return message + ''.join([chr(p)] * p)
    elif isinstance(message, bytes):
        return message + bytes([p]) * p
    else:
        raise TypeError("pad doesn't know how to handle type " + type(message).__name__)


def unpad(message, method = "PKCS#7"):
    if method == "PKCS#7":
        # STRING INPUT
        if isinstance(message, str):
            # pick value of last byte
            pad_char = message[len(message) - 1]
            n = int(pad_char.encode('ascii').hex(), 16)
            # handle unpadded messages
            if message[(len(message) - n):] == pad_char*n:
                return message[:(len(message)-n)]
            else:
                raise Exception('invalid message padding')
        # BYTES INPUT
        elif isinstance(message, bytes):
            n = message[len(message)-1]
            # handle unpadded messages
            if message[(len(message) - n):] == bytes([n]*n):
                return message[:(len(message)-n)]
            else:
                raise Exception('invalid message padding')
        else:
            raise TypeError("pad doesn't know how to handle type " + type(message).__name__)


if __name__ == '__main__':
    assert pad("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04"
    assert unpad(pad("YELLOW SUBMARINE", 20)) == "YELLOW SUBMARINE"
    assert pad("YELLOW SUBMARINE", 16) == "YELLOW SUBMARINE" + '\x10'*16

    assert pad(b"YELLOW SUBMARINE", 20) == b"YELLOW SUBMARINE\x04\x04\x04\x04"
    assert unpad(pad(b"YELLOW SUBMARINE", 20)) == b"YELLOW SUBMARINE"
    assert pad(b"YELLOW SUBMARINE", 16) == b"YELLOW SUBMARINE" + b'\x10'*16

    # invalid pads
    assert unpad("YELLOW SUBMARINE\x03\x03") == "YELLOW SUBMARINE\x03\x03"
    assert unpad(b"YELLOW SUBMARINE\x03\x03") == b"YELLOW SUBMARINE\x03\x03"
