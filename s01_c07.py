import base64

# easy way
from Crypto.Cipher import AES
import base64
ciphertext = open('s01_c07_input.txt').read().replace('\n', '')
cipherbytes = base64.decodebytes(bytes(ciphertext.encode()))
cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
plaintext = cipher.decrypt(cipherbytes)


# hard way

def xor(a:'bytes', b:'bytes') -> 'bytes':
    if len(a) != len(b):
        raise ValueError('inputs must have same length')

    return b''.join([(a[i] ^ b[i]).to_bytes(1, 'big') for i in range(len(a))])


def bitstring_to_bytes(s):
    """
    from PM 2 Ring on stack exchange
    :param s:
    :return:
    """
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def SubBytes(state:'bytes') -> 'bytes':
    # sub bytes, lookup from fig 7 of spec
    s_box = {'00000000': '01100011', '00000001': '01111100', '00000010': '01110111', '00000011': '01111011',
             '00000100': '11110010', '00000101': '01101011', '00000110': '01101111', '00000111': '11000101',
             '00001000': '00110000', '00001001': '00000001', '00001010': '01100111', '00001011': '00101011',
             '00001100': '11111110', '00001101': '11010111', '00001110': '10101011', '00001111': '01110110',
             '00010000': '11001010', '00010001': '10000010', '00010010': '11001001', '00010011': '01111101',
             '00010100': '11111010', '00010101': '01011001', '00010110': '01000111', '00010111': '11110000',
             '00011000': '10101101', '00011001': '11010100', '00011010': '10100010', '00011011': '10101111',
             '00011100': '10011100', '00011101': '10100100', '00011110': '01110010', '00011111': '11000000',
             '00100000': '10110111', '00100001': '11111101', '00100010': '10010011', '00100011': '00100110',
             '00100100': '00110110', '00100101': '00111111', '00100110': '11110111', '00100111': '11001100',
             '00101000': '00110100', '00101001': '10100101', '00101010': '11100101', '00101011': '11110001',
             '00101100': '01110001', '00101101': '11011000', '00101110': '00110001', '00101111': '00010101',
             '00110000': '00000100', '00110001': '11000111', '00110010': '00100011', '00110011': '11000011',
             '00110100': '00011000', '00110101': '10010110', '00110110': '00000101', '00110111': '10011010',
             '00111000': '00000111', '00111001': '00010010', '00111010': '10000000', '00111011': '11100010',
             '00111100': '11101011', '00111101': '00100111', '00111110': '10110010', '00111111': '01110101',
             '01000000': '00001001', '01000001': '10000011', '01000010': '00101100', '01000011': '00011010',
             '01000100': '00011011', '01000101': '01101110', '01000110': '01011010', '01000111': '10100000',
             '01001000': '01010010', '01001001': '00111011', '01001010': '11010110', '01001011': '10110011',
             '01001100': '00101001', '01001101': '11100011', '01001110': '00101111', '01001111': '10000100',
             '01010000': '01010011', '01010001': '11010001', '01010010': '00000000', '01010011': '11101101',
             '01010100': '00100000', '01010101': '11111100', '01010110': '10110001', '01010111': '01011011',
             '01011000': '01101010', '01011001': '11001011', '01011010': '10111110', '01011011': '00111001',
             '01011100': '01001010', '01011101': '01001100', '01011110': '01011000', '01011111': '11001111',
             '01100000': '11010000', '01100001': '11101111', '01100010': '10101010', '01100011': '11111011',
             '01100100': '01000011', '01100101': '01001101', '01100110': '00110011', '01100111': '10000101',
             '01101000': '01000101', '01101001': '11111001', '01101010': '00000010', '01101011': '01111111',
             '01101100': '01010000', '01101101': '00111100', '01101110': '10011111', '01101111': '10101000',
             '01110000': '01010001', '01110001': '10100011', '01110010': '01000000', '01110011': '10001111',
             '01110100': '10010010', '01110101': '10011101', '01110110': '00111000', '01110111': '11110101',
             '01111000': '10111100', '01111001': '10110110', '01111010': '11011010', '01111011': '00100001',
             '01111100': '00010000', '01111101': '11111111', '01111110': '11110011', '01111111': '11010010',
             '10000000': '11001101', '10000001': '00001100', '10000010': '00010011', '10000011': '11101100',
             '10000100': '01011111', '10000101': '10010111', '10000110': '01000100', '10000111': '00010111',
             '10001000': '11000100', '10001001': '10100111', '10001010': '01111110', '10001011': '00111101',
             '10001100': '01100100', '10001101': '01011101', '10001110': '00011001', '10001111': '01110011',
             '10010000': '01100000', '10010001': '10000001', '10010010': '01001111', '10010011': '11011100',
             '10010100': '00100010', '10010101': '00101010', '10010110': '10010000', '10010111': '10001000',
             '10011000': '01000110', '10011001': '11101110', '10011010': '10111000', '10011011': '00010100',
             '10011100': '11011110', '10011101': '01011110', '10011110': '00001011', '10011111': '11011011',
             '10100000': '11100000', '10100001': '00110010', '10100010': '00111010', '10100011': '00001010',
             '10100100': '01001001', '10100101': '00000110', '10100110': '00100100', '10100111': '01011100',
             '10101000': '11000010', '10101001': '11010011', '10101010': '10101100', '10101011': '01100010',
             '10101100': '10010001', '10101101': '10010101', '10101110': '11100100', '10101111': '01111001',
             '10110000': '11100111', '10110001': '11001000', '10110010': '00110111', '10110011': '01101101',
             '10110100': '10001101', '10110101': '11010101', '10110110': '01001110', '10110111': '10101001',
             '10111000': '01101100', '10111001': '01010110', '10111010': '11110100', '10111011': '11101010',
             '10111100': '01100101', '10111101': '01111010', '10111110': '10101110', '10111111': '00001000',
             '11000000': '10111010', '11000001': '01111000', '11000010': '00100101', '11000011': '00101110',
             '11000100': '00011100', '11000101': '10100110', '11000110': '10110100', '11000111': '11000110',
             '11001000': '11101000', '11001001': '11011101', '11001010': '01110100', '11001011': '00011111',
             '11001100': '01001011', '11001101': '10111101', '11001110': '10001011', '11001111': '10001010',
             '11010000': '01110000', '11010001': '00111110', '11010010': '10110101', '11010011': '01100110',
             '11010100': '01001000', '11010101': '00000011', '11010110': '11110110', '11010111': '00001110',
             '11011000': '01100001', '11011001': '00110101', '11011010': '01010111', '11011011': '10111001',
             '11011100': '10000110', '11011101': '11000001', '11011110': '00011101', '11011111': '10011110',
             '11100000': '11100001', '11100001': '11111000', '11100010': '10011000', '11100011': '00010001',
             '11100100': '01101001', '11100101': '11011001', '11100110': '10001110', '11100111': '10010100',
             '11101000': '10011011', '11101001': '00011110', '11101010': '10000111', '11101011': '11101001',
             '11101100': '11001110', '11101101': '01010101', '11101110': '00101000', '11101111': '11011111',
             '11110000': '10001100', '11110001': '10100001', '11110010': '10001001', '11110011': '00001101',
             '11110100': '10111111', '11110101': '11100110', '11110110': '01000010', '11110111': '01101000',
             '11111000': '01000001', '11111001': '10011001', '11111010': '00101101', '11111011': '00001111',
             '11111100': '10110000', '11111101': '01010100', '11111110': '10111011', '11111111': '00010110'}

    return b''.join([bitstring_to_bytes(s_box.get(bin(byte)[2:].rjust(8, '0'))) for byte in state])


def RotWord(word):
    return word[1:] + word[:1]


def KeyExpansion(key:'bytes', Nk:'32 bit key blocks'=4):
    # define round constants
    Rcon = [b'\x01\x00\x00\x00', b'\x02\x00\x00\x00',
            b'\x04\x00\x00\x00', b'\x08\x00\x00\x00',
            b'\x10\x00\x00\x00', b' \x00\x00\x00',
            b'@\x00\x00\x00'   , b'\x80\x00\x00\x00',
            b'\x1b\x00\x00\x00', b'6\x00\x00\x00']


    # initialize expanded words
    w = [None] * (4 * (10 + 1))

    # first Nk words are the key in 4byte blocks
    for i in range(0, Nk):
        w[i] = key[(4*i):(4*(i+1))]
    # after that, XOR of word w[i-1] and w[i-Nk], but if i % Nk == 0, transform w[i-1] first
    # transform is RotWord then SubWord on the bytes, then XOR round constant Rcon[i]
    for i in range(Nk, 4 * (10 + 1)):
        if i % Nk == 0:
            temp_word = xor(SubBytes(RotWord(w[i-1])), Rcon[(i // Nk) - 1])
        else:
            temp_word = w[i-1]
        w[i] = xor(temp_word, w[i-Nk])

    return w


def ShiftRows(state):
    # note the index is weird cause it's by column not row
    # 0 4 8  12    0  4  8  12
    # 1 5 9  13 -> 5  9  13 1
    # 2 6 10 14    10 14 2  6
    # 3 7 11 15    15 3  7  11
    new_state = b''.join([state[i].to_bytes(1, 'big') for i in [0, 5, 10, 15,
                                                                4, 9, 14, 3,
                                                                8, 13, 2, 7,
                                                                12, 1, 6, 11]])

    return new_state


def MultGF(a, b):
    """
    multiplication in GF(2^8)
    peasant's algorithm (thanks, wikipedia)
    :param a:
    :param b:
    :return:
    """
    p = '00000000'

    for i in range(0, 8):
        # stop if a or b is 0
        if(a == '00000000' or b == '00000000'):
            break
        # if b's trailing bit is 1, xor p and a (addition in this field)
        if(b[7] == '1'):
            p = xor(p, a)
        # shift b one bit right (this divides by x)
        b = '0' + b[:7]
        # set carry flag as leftmost bit of a
        carry = a[0]
        # shift a one bit left (multiply by x)
        a = a[1:] + '0'
        # if carry, xor a with 0x1b (the irreducible polynomial without the x^8 term)
        if(carry == '1'):
            a = xor(a, '00011011')

    return p


def MixColumns(s):
    # initialize
    new_state = [''] * 16

    # each column, xor is commutative so no worries about that order
    for i in range(0, 4):
        new_state[4*i]   = xor(xor(xor(MultGF('00000010', s[4*i]), MultGF('00000011', s[4*i+1])), s[4*i+2]), s[4*i+3])
        new_state[4*i+1] = xor(xor(xor(s[4*i], MultGF('00000010', s[4*i+1])), MultGF('00000011', s[4*i+2])), s[4*i+3])
        new_state[4*i+2] = xor(xor(xor(s[4*i], s[4*i+1]), MultGF('00000010', s[4*i+2])), MultGF('00000011', s[4*i+3]))
        new_state[4*i+3] = xor(xor(xor(MultGF('00000011', s[4*i]), s[4*i+1]), s[4*i+2]), MultGF('00000010', s[4*i+3]))

    return new_state


def MakeRoundKeys(exp_key, rounds = 11):
    """
    make round key lists from expanded keys

    :param exp_key:
    :param rounds: lazily making this 11 since i'm doing 128 bit, hopefully doesn't bite me later
    :return:
    """
    return [b''.join(exp_key[(4*i):(4*(i+1))]) for i in range(0, rounds)]


def AddRoundKey(state, round_key):
    return xor(state, round_key)


def EncryptAES(message, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes (for AES-128, I didn't implement others)")

    # get round keys
    round_keys = MakeRoundKeys(exp_key=KeyExpansion(key, Nk=4), rounds=11)

    # convert message to blocks, padding last block with 0s if needed
    msg_blocks = [message[i:i+16] for i in range(0, len(message), 16)]
    msg_blocks[len(msg_blocks)-1] + b''.join([b'0' for i in range(0, 16 - len(msg_blocks[len(msg_blocks)-1]))])

    cipher_blocks = [None] * len(msg_blocks)

    for m in range(len(cipher_blocks)):
        state = msg_blocks[m]

        # round 0
        state = AddRoundKey(state, round_keys[0])

        # rounds 1-10
        for r in range(1, 11):
            state = SubBytes(state)
            state = ShiftRows(state)
            # mix columns omitted for last round
            if(r != 10):
                state = MixColumns(state)

            state = AddRoundKey(state, round_keys[r])
            # hex_state = ' '.join([bin_to_hex(a) for a in state])

        cipher_blocks[m] = ''.join(state)

    return ''.join(cipher_blocks)


def InvShiftRows(state):
    # note the index is weird cause it's by column not row
    # 0 4 8  12    0  4  8  12
    # 1 5 9  13 -> 13 1  5  9
    # 2 6 10 14    10 14 2  6
    # 3 7 11 15    7  11 15 3
    new_state = [state[i] for i in [0, 13, 10, 7,
                                    4,  1, 14, 11,
                                    8,  5, 2,  15,
                                    12, 9, 6,  3]]

    return new_state


def InvSubBytes(state):
    # now that i implemented GF multiplication i could do that, but i already have the old lookup to invert
    inv_s_box = {'01100011': '00000000', '01111100': '00000001', '01110111': '00000010', '01111011': '00000011',
                 '11110010': '00000100', '01101011': '00000101', '01101111': '00000110', '11000101': '00000111',
                 '00110000': '00001000', '00000001': '00001001', '01100111': '00001010', '00101011': '00001011',
                 '11111110': '00001100', '11010111': '00001101', '10101011': '00001110', '01110110': '00001111',
                 '11001010': '00010000', '10000010': '00010001', '11001001': '00010010', '01111101': '00010011',
                 '11111010': '00010100', '01011001': '00010101', '01000111': '00010110', '11110000': '00010111',
                 '10101101': '00011000', '11010100': '00011001', '10100010': '00011010', '10101111': '00011011',
                 '10011100': '00011100', '10100100': '00011101', '01110010': '00011110', '11000000': '00011111',
                 '10110111': '00100000', '11111101': '00100001', '10010011': '00100010', '00100110': '00100011',
                 '00110110': '00100100', '00111111': '00100101', '11110111': '00100110', '11001100': '00100111',
                 '00110100': '00101000', '10100101': '00101001', '11100101': '00101010', '11110001': '00101011',
                 '01110001': '00101100', '11011000': '00101101', '00110001': '00101110', '00010101': '00101111',
                 '00000100': '00110000', '11000111': '00110001', '00100011': '00110010', '11000011': '00110011',
                 '00011000': '00110100', '10010110': '00110101', '00000101': '00110110', '10011010': '00110111',
                 '00000111': '00111000', '00010010': '00111001', '10000000': '00111010', '11100010': '00111011',
                 '11101011': '00111100', '00100111': '00111101', '10110010': '00111110', '01110101': '00111111',
                 '00001001': '01000000', '10000011': '01000001', '00101100': '01000010', '00011010': '01000011',
                 '00011011': '01000100', '01101110': '01000101', '01011010': '01000110', '10100000': '01000111',
                 '01010010': '01001000', '00111011': '01001001', '11010110': '01001010', '10110011': '01001011',
                 '00101001': '01001100', '11100011': '01001101', '00101111': '01001110', '10000100': '01001111',
                 '01010011': '01010000', '11010001': '01010001', '00000000': '01010010', '11101101': '01010011',
                 '00100000': '01010100', '11111100': '01010101', '10110001': '01010110', '01011011': '01010111',
                 '01101010': '01011000', '11001011': '01011001', '10111110': '01011010', '00111001': '01011011',
                 '01001010': '01011100', '01001100': '01011101', '01011000': '01011110', '11001111': '01011111',
                 '11010000': '01100000', '11101111': '01100001', '10101010': '01100010', '11111011': '01100011',
                 '01000011': '01100100', '01001101': '01100101', '00110011': '01100110', '10000101': '01100111',
                 '01000101': '01101000', '11111001': '01101001', '00000010': '01101010', '01111111': '01101011',
                 '01010000': '01101100', '00111100': '01101101', '10011111': '01101110', '10101000': '01101111',
                 '01010001': '01110000', '10100011': '01110001', '01000000': '01110010', '10001111': '01110011',
                 '10010010': '01110100', '10011101': '01110101', '00111000': '01110110', '11110101': '01110111',
                 '10111100': '01111000', '10110110': '01111001', '11011010': '01111010', '00100001': '01111011',
                 '00010000': '01111100', '11111111': '01111101', '11110011': '01111110', '11010010': '01111111',
                 '11001101': '10000000', '00001100': '10000001', '00010011': '10000010', '11101100': '10000011',
                 '01011111': '10000100', '10010111': '10000101', '01000100': '10000110', '00010111': '10000111',
                 '11000100': '10001000', '10100111': '10001001', '01111110': '10001010', '00111101': '10001011',
                 '01100100': '10001100', '01011101': '10001101', '00011001': '10001110', '01110011': '10001111',
                 '01100000': '10010000', '10000001': '10010001', '01001111': '10010010', '11011100': '10010011',
                 '00100010': '10010100', '00101010': '10010101', '10010000': '10010110', '10001000': '10010111',
                 '01000110': '10011000', '11101110': '10011001', '10111000': '10011010', '00010100': '10011011',
                 '11011110': '10011100', '01011110': '10011101', '00001011': '10011110', '11011011': '10011111',
                 '11100000': '10100000', '00110010': '10100001', '00111010': '10100010', '00001010': '10100011',
                 '01001001': '10100100', '00000110': '10100101', '00100100': '10100110', '01011100': '10100111',
                 '11000010': '10101000', '11010011': '10101001', '10101100': '10101010', '01100010': '10101011',
                 '10010001': '10101100', '10010101': '10101101', '11100100': '10101110', '01111001': '10101111',
                 '11100111': '10110000', '11001000': '10110001', '00110111': '10110010', '01101101': '10110011',
                 '10001101': '10110100', '11010101': '10110101', '01001110': '10110110', '10101001': '10110111',
                 '01101100': '10111000', '01010110': '10111001', '11110100': '10111010', '11101010': '10111011',
                 '01100101': '10111100', '01111010': '10111101', '10101110': '10111110', '00001000': '10111111',
                 '10111010': '11000000', '01111000': '11000001', '00100101': '11000010', '00101110': '11000011',
                 '00011100': '11000100', '10100110': '11000101', '10110100': '11000110', '11000110': '11000111',
                 '11101000': '11001000', '11011101': '11001001', '01110100': '11001010', '00011111': '11001011',
                 '01001011': '11001100', '10111101': '11001101', '10001011': '11001110', '10001010': '11001111',
                 '01110000': '11010000', '00111110': '11010001', '10110101': '11010010', '01100110': '11010011',
                 '01001000': '11010100', '00000011': '11010101', '11110110': '11010110', '00001110': '11010111',
                 '01100001': '11011000', '00110101': '11011001', '01010111': '11011010', '10111001': '11011011',
                 '10000110': '11011100', '11000001': '11011101', '00011101': '11011110', '10011110': '11011111',
                 '11100001': '11100000', '11111000': '11100001', '10011000': '11100010', '00010001': '11100011',
                 '01101001': '11100100', '11011001': '11100101', '10001110': '11100110', '10010100': '11100111',
                 '10011011': '11101000', '00011110': '11101001', '10000111': '11101010', '11101001': '11101011',
                 '11001110': '11101100', '01010101': '11101101', '00101000': '11101110', '11011111': '11101111',
                 '10001100': '11110000', '10100001': '11110001', '10001001': '11110010', '00001101': '11110011',
                 '10111111': '11110100', '11100110': '11110101', '01000010': '11110110', '01101000': '11110111',
                 '01000001': '11111000', '10011001': '11111001', '00101101': '11111010', '00001111': '11111011',
                 '10110000': '11111100', '01010100': '11111101', '10111011': '11111110', '00010110': '11111111'}

    return [inv_s_box.get(byte) for byte in state]


def InvMixColumns(s):
    # initialize
    new_state = [''] * 16

    # each column, xor is commutative so no worries about that order
    for i in range(0, 4):
        new_state[4 * i]     = xor(xor(xor(MultGF('00001110', s[4*i]),
                                           MultGF('00001011', s[4*i+1])),
                                       MultGF('00001101', s[4*i+2])),
                                   MultGF('00001001', s[4*i+3]))
        new_state[4 * i + 1] = xor(xor(xor(MultGF('00001001', s[4*i]),
                                           MultGF('00001110', s[4*i+1])),
                                       MultGF('00001011', s[4*i+2])),
                                   MultGF('00001101', s[4*i+3]))
        new_state[4 * i + 2] = xor(xor(xor(MultGF('00001101', s[4*i]),
                                           MultGF('00001001', s[4*i+1])),
                                       MultGF('00001110', s[4*i+2])),
                                   MultGF('00001011', s[4*i+3]))
        new_state[4 * i + 3] = xor(xor(xor(MultGF('00001011', s[4*i]),
                                           MultGF('00001101', s[4*i+1])),
                                       MultGF('00001001', s[4*i+2])),
                                   MultGF('00001110', s[4*i+3]))

    return new_state


def DecryptAES(bcipher, bkey):
    """
    not using the cooler equivalent inverse cause i don't want to make a different key schedule too
    :param bcipher:
    :param bkey:
    :return:
    """

    if len(bkey) != 8*16:
        ValueError

    # get round keys
    round_keys = MakeRoundKeys(exp_key=KeyExpansion(bkey, Nk=4), rounds=11)

    # convert message to blocks
    msg_blocks = pad_blocks(block_string(bcipher, 128, 'front'), 128, 'back', '0')

    cipher_blocks = [None] * len(msg_blocks)

    for m in range(len(cipher_blocks)):
        state = MakeState(msg_blocks[m])
        hex_state = ' '.join([bin_to_hex(a) for a in state])

        # undo rounds 11-2
        for r in range(10, 0, -1):
            state = AddRoundKey(state, round_keys[r])
            hex_state = ' '.join([bin_to_hex(a) for a in state])
            if r != 10:
                state = InvMixColumns(state)
                hex_state = ' '.join([bin_to_hex(a) for a in state])
            state = InvShiftRows(state)
            hex_state = ' '.join([bin_to_hex(a) for a in state])
            state = InvSubBytes(state)
            hex_state = ' '.join([bin_to_hex(a) for a in state])

        # undo round 1
        state = AddRoundKey(state, round_keys[0])
        hex_state = ' '.join([bin_to_hex(a) for a in state])

        cipher_blocks[m] = ''.join(state)

    return ''.join(cipher_blocks)


if __name__ == '__main__':
    # test new xor
    input = 'ead27321'
    blocks = [input[i:i+2] for i in range(0, len(input), 2)]
    b''.join([int(b, 16).to_bytes(1, 'big') for b in blocks])
    assert xor(b'\x1c\x01\x11\x00\x1f\x01\x01\x00\x06\x1a\x02KSSP\t\x18\x1c',
               b"hit the bull's eye") == b"the kid don't play"

    # test KeyExpansion (appendix A)
    key = b'+~\x15\x16(\xae\xd2\xa6\xab\xf7\x15\x88\t\xcfO<'
    exp_key = [w for w in KeyExpansion(key)]
    assert exp_key[2]  == b'\xab\xf7\x15\x88'
    assert exp_key[15] == b'mz\x88;'
    assert exp_key[32] == b'\xea\xd2s!'

    # LEFT OFF HERE------------------
    # GF(2^8) multiplication
    assert MultGF('01010011', '11001010') == '00000001'
    # probably need more tests here

    # cipher example from appendix B
    input = '3243f6a8885a308d313198a2e0370734'
    key   = '2b7e151628aed2a6abf7158809cf4f3c'

    exp_keys = KeyExpansion(hex_to_bin(key))
    round_keys = MakeRoundKeys(exp_keys)

    # encrypt tests (on round 1)
    start_round       = block_string(hex_to_bin('193de3bea0f4e22b9ac68d2ae9f84808'), 8, 'front')
    after_SubBytes    = block_string(hex_to_bin('d42711aee0bf98f1b8b45de51e415230'), 8, 'front')
    after_ShiftRows   = block_string(hex_to_bin('d4bf5d30e0b452aeb84111f11e2798e5'), 8, 'front')
    after_MixColumns  = block_string(hex_to_bin('046681e5e0cb199a48f8d37a2806264c'), 8, 'front')
    round_key         = block_string(hex_to_bin('a0fafe1788542cb123a339392a6c7605'), 8, 'front')
    after_AddRoundKey = block_string(hex_to_bin('a49c7ff2689f352b6b5bea43026a5049'), 8, 'front')

    assert start_round == block_string(xor(hex_to_bin(input), hex_to_bin(key)), 8, 'front')
    assert SubBytes(start_round) == after_SubBytes
    assert ShiftRows(after_SubBytes) == after_ShiftRows
    assert MixColumns(after_ShiftRows) == after_MixColumns
    assert round_key == round_keys[1]
    assert AddRoundKey(after_MixColumns, round_keys[1]) == after_AddRoundKey
    assert EncryptAES(hex_to_bin(input), hex_to_bin(key)) == hex_to_bin('3925841d02dc09fbdc118597196a0b32')

    # decrypt tests (on round 1)
    assert InvShiftRows(after_ShiftRows) == after_SubBytes
    assert InvSubBytes(after_SubBytes) == start_round
    assert InvMixColumns(after_MixColumns) == after_ShiftRows
    assert DecryptAES(hex_to_bin('3925841d02dc09fbdc118597196a0b32'), hex_to_bin(key)) == hex_to_bin(input)

    # test encrypt something
    de_la_plaintext  = open("./de_la_test.txt", "r").read()
    message = de_la_plaintext.encode('ascii')
    key = "YELLOW SUBMARINE".encode('ascii')


    # decode the prompt
    my_ciphertext = open('s01_c07_input.txt').read().replace('\n', '')
    key = "YELLOW SUBMARINE"
    plaintext = DecryptAES(b64_to_bin(ciphertext), ascii_to_bin(key))
    print(bin_to_ascii(plaintext))

    # troubleshoot decrypt
    test_plain = "I'm back and I'm ringing the bell"
    test_crypt = EncryptAES(ascii_to_bin(test_plain), ascii_to_bin("YELLOW SUBMARINE"))
    a = DecryptAES(test_crypt, ascii_to_bin("YELLOW SUBMARINE"))

# or i guess here's how they intended...i thought 'in code' meant do it yourself
from Crypto.Cipher import AES
import base64
ciphertext = open('s01_c07_input.txt').read().replace('\n', '')
cipherbytes = base64.decodebytes(bytes(ciphertext.encode()))
cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
plaintext = cipher.decrypt(cipherbytes)

# test 1 - encode a single 16-byte message
from Crypto.Util.Padding import pad, unpad

plaintext = 'this message is 32 bytes longggg'
key       = 'YELLOW SUBMARINE'
true_encode = cipher.encrypt(plaintext.encode('ascii'))
my_encode   = EncryptAES(ascii_to_bin(plaintext), ascii_to_bin(key))
assert true_encode.hex() == bin_to_hex(my_encode)

# test 2 - decode that single 16-byte message
true_decode = cipher.decrypt(true_encode)
my_decode = bin_to_ascii(DecryptAES(my_encode, ascii_to_bin(key)))
