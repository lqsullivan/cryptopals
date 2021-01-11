# update PKCS#7 padding functions

def unpad(message):
    pad_char = message[len(message)-1]
    n = ord(pad_char)

    if message[len(message)-n:] == pad_char*n :
        return message[:len(message)-n]
    else:
        raise Exception("invalid message padding")

if __name__ == '__main__':
    assert unpad("ICE ICE BABY\x04\x04\x04\x04") == "ICE ICE BABY"
    # should figure out how to unit test raised exceptions eventually
    unpad("ICE ICE BABY\x01\x02\x03\x04")