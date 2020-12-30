# PKCS#7 padding

def pad(plaintext, n, method = "PKCS#7"):
    """
    pads to the nearest multiple of block size

    :param plaintext:
    :param n:
    :param method:
    :return:
    """

    if method == "PKCS#7":
        if n > 255:
            raise ValueError('For PKCS#7 padding, block size must be <256')
        # pad with number of bytes added
        p = ((len(plaintext) // n) + 1) * n

    return plaintext.ljust(p, chr(p - len(plaintext)))

if __name__ == '__main__':
    assert pad("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04"