# PKCS#7 padding

def pad(message, n, method = "PKCS#7"):
    if method == "PKCS#7":
        if n > 255:
            raise ValueError('For PKCS#7 padding, block size must be <256')
        # pad with number of bytes added
        p = ((len(message) // n) + 1) * n

    return message.ljust(p, chr(p - len(message)))


def unpad(message, method = "PKCS#7"):
    if method == "PKCS#7":
        # pick value of last byte
        n_pad = int(message[len(message)-1].encode().hex(), 16)

    # remove that many bytes
    return message[:(len(message) - n_pad)]

if __name__ == '__main__':
    assert pad("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04"
    assert unpad(pad("YELLOW SUBMARINE", 20)) == "YELLOW SUBMARINE"