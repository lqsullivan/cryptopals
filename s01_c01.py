from base64 import b64encode, b64decode

def block_string(string, n, type):
    """
    :param string: input string
    :param n: size of blocks
    :param type: 'front' or 'back', direction to begin making blocks from
    also determines where pad_char will go, end or beginning of blocks
    :return:
    """
    # note the upside-down floor division in the range
    if type == 'front':
        out = [string[(n * i):min((n * (i + 1)), len(string))] for i in range(0, -(-len(string) // n))]
    elif type == 'back':
        out = [string[max(0, (len(string) - n * (i + 1))):(len(string) - n * i)] for i in
               range(0, -(-len(string) // n))]
        # reverse list to get in right order
        out.reverse()
    else:
        raise ValueError('start_from must be front or back')

    return out

def pad_blocks(blocks, n, type, pad_char = '0'):
    """
    pad elements of list to a size (or truncate those not at size)
    :param blocks:
    :param n:
    :param type:
    :param pad_char:
    :return:
    """
    if type == 'front':
        out = [block.rjust(n, pad_char) for block in blocks]
    elif type == 'back':
        out = [block.ljust(n, pad_char) for block in blocks]
    elif type == 'trunc':
        out = [block for block in blocks if len(block) == n]
    else:
        raise ValueError('pad type must be front back or trunc')

    return out

def bin_to_hex(bstring):
    out = ''.join([hex(int(byte, 2))[2:].rjust(2, '0') for byte in pad_blocks(block_string(bstring, n=8, type='front'), 8, 'front', '0')])
    return out

def hex_to_bin(hstring):
    """
    convert hex string to binary string
    :param hex:
    :return:
    """
    hblock = block_string(hstring, n=2, type='front')
    bblock = [bin(int(h, 16))[2:] for h in hblock]
    out = ''.join(pad_blocks(bblock, n=8, type='front', pad_char='0'))

    return out

def hex_to_ascii(hstring):
    out = ''.join([chr(int(hex, 16)) for hex in pad_blocks(block_string(hstring, n=2, type='back'), 2, 'front', '0')])
    return out

def ascii_to_hex(string):
    out = string.encode('ascii').hex()
    #out = ''.join([hex(ord(char))[2:] for char in string])
    return out

def bin_to_ascii(bstring):
    out = ''.join([chr(int(byte, 2)) for byte in pad_blocks(block_string(bstring, n=8, type='back'), 8, 'front', '0')])
    return out

def ascii_to_bin(string):
    out = hex_to_bin(string.encode('ascii').hex())
    return out

def hex_to_b64(hstring):
    """
    converts a hex-encoded string to base 64
    :param hstring: hex string
    :return: b64 string
    """

    # convert hex to binary
    bstring = hex_to_bin(hstring)

    # separate into chunks of 6 bits
    bin_blocks = block_string(bstring, n=6, type='front')
    bin_blocks = pad_blocks(bin_blocks, n=6, type='back', pad_char='0')

    # convert binary to b64 by indexing in the ordered string
    b64_to_hex_lookup = "ABCDEFGHIJLKMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    out = ''.join([b64_to_hex_lookup[int(block, 2)] for block in bin_blocks])

    return out

def b64_to_hex(b64string):
    """
    converts base64 string to hex string
    :param b64:
    :return:
    """
    # strip padding
    b64string = b64string.strip('=')
    b64_to_hex_lookup = "ABCDEFGHIJLKMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    # find integer value of b64 char
    # convert to bin (pad to 6)
    b64_idx = [b64_to_hex_lookup.find(char) for char in b64string]

    if any([idx == -1 for idx in b64_idx]):
        print("input string contains non-b64 character")
        raise ValueError

    bstring = ''.join([bin(char)[2:].rjust(6, "0") for char in b64_idx])
    # split into 4s and hex
    bin_blocks = block_string(bstring, 8, type='front')
    bin_blocks = pad_blocks(bin_blocks, n = 8, type = 'trunc')
    out = ''.join([hex(int(block, 2))[2:].rjust(2, '0') for block in bin_blocks])

    return out

def b64_to_bin(b64string):
    out = hex_to_bin(b64_to_hex(b64string))
    return out

def bin_to_b64(bstring):
    out = hex_to_b64(bin_to_hex(bstring))
    return out

def ascii_to_b64(string):
    out = bin_to_b64(ascii_to_bin(string))
    return out

def b64_to_ascii(b64string):
    out = bin_to_ascii(b64_to_bin(b64string))
    return out

# challenge ----
if __name__ == '__main__':
    assert hex_to_b64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d") == \
           "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    assert b64_to_hex("SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t") == \
           "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

    assert ascii_to_hex('Ma') == '4d61'
    assert hex_to_ascii('4d61') == 'Ma'
    assert ascii_to_bin('Ma') == '0100110101100001'
    assert bin_to_ascii('0100110101100001') == 'Ma'
    assert ascii_to_b64('Ma') == 'TWE'
    assert b64_to_ascii('TWE=') == 'Ma'

    assert b64_to_hex('HUIfTQsPAh9PE048Gmll') == '1d421f4d0b0f021f4f134e3c1a6965'
    assert hex_to_b64('1d421f4d0b0f021f4f134e3c1a6965') == 'HUIfTQsPAh9PE048Gmll'

    assert b64_to_bin('HUIfTQsPAh9PE048Gmll') == '000111010100001000011111010011010000101100001111000000100001111101001111000100110100111000111100000110100110100101100101'
    assert bin_to_b64('000111010100001000011111010011010000101100001111000000100001111101001111000100110100111000111100000110100110100101100101') == 'HUIfTQsPAh9PE048Gmll'

    from base64 import b64decode, b64encode
    assert b64decode('longertest==').hex() == b64_to_hex('longertest==')

    assert hex_to_ascii(b64_to_hex('YW55IGNhcm5hbCBwbGVhc3Vy')) == 'any carnal pleasur'
    assert hex_to_ascii(b64_to_hex('YW55IGNhcm5hbCBwbGVhc3U=')) == 'any carnal pleasu'
    assert hex_to_ascii(b64_to_hex('YW55IGNhcm5hbCBwbGVhcw==')) == 'any carnal pleas'
