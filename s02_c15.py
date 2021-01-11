from s02_c09 import unpad

if __name__ == '__main__':
    assert unpad("ICE ICE BABY\x04\x04\x04\x04") == "ICE ICE BABY"
    # should figure out how to unit test raised exceptions eventually
    unpad("ICE ICE BABY\x01\x02\x03\x04")