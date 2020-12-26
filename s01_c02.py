# fixed XOR

def xor(bstr1, bstr2):
    out = int(bstr1, 2) ^ int(bstr2, 2)

    return bin(out)[2:].rjust(bstr1.__len__(), "0")

def hex_xor(hstr1, hstr2):
    out = int(hstr1, 16) ^ int(hstr2, 16)

    # convert back to hex
    return hex(out)[2:]

# challenge ----
if __name__ == '__main__':
    assert hex_xor("1c0111001f010100061a024b53535009181c",
               "686974207468652062756c6c277320657965") ==\
        "746865206b696420646f6e277420706c6179"