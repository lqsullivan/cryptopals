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
            p = 0
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
        if isinstance(message, str):
            # pick value of last byte
            n_pad = int(message[len(message) - 1].encode().hex(), 16)
            # handle unpadded messages
            if message[(len(message) - n_pad):] != bytes([n_pad] * n_pad).decode('ascii'):
                return message
        elif isinstance(message, bytes):
            n_pad = message[len(message)-1]
            # handle unpadded messages
            if message[(len(message) - n_pad):] != bytes([n_pad] * n_pad):
                return message
        else:
            raise TypeError("pad doesn't know how to handle type " + type(message).__name__)

    # remove that many bytes
    return message[:(len(message) - n_pad)]

if __name__ == '__main__':
    assert pad("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04"
    assert unpad(pad("YELLOW SUBMARINE", 20)) == "YELLOW SUBMARINE"
    assert unpad("YELLOW SUBMARINE\x03\x03") == "YELLOW SUBMARINE\x03\x03"
    assert pad("YELLOW SUBMARINE", 16) == "YELLOW SUBMARINE"

    assert pad(b"YELLOW SUBMARINE", 20) == b"YELLOW SUBMARINE\x04\x04\x04\x04"
    assert unpad(pad(b"YELLOW SUBMARINE", 20)) == b"YELLOW SUBMARINE"
    assert unpad(b"YELLOW SUBMARINE\x03\x03") == b"YELLOW SUBMARINE\x03\x03"
    assert pad(b"YELLOW SUBMARINE", 16) == b"YELLOW SUBMARINE"
