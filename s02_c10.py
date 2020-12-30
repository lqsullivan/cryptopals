from s01_c07 import xor
from Crypto.Cipher import AES

# ECB mode: break plaintext into blocks, use the block cipher on each block
# CBC mode: break plaintext into blocks, xor with last ciphertext block, then apply block cipher

# we want to use the AES block cipher in CBC mode here
def encrypt_aes_cbc(plaintext, key, iv):
    # break plaintext into chunks
    msg_blocks = [plaintext[i:i + 16] for i in range(0, len(plaintext), 16)]
    msg_blocks[len(msg_blocks) - 1] = msg_blocks[len(msg_blocks) - 1] + \
                                      b''.join([b'0' for i in range(0, 16 - len(msg_blocks[len(msg_blocks) - 1]))])

    # set up block cipher
    cipher = AES.new(key, AES.MODE_ECB)

    # initialize encrypted blocks
    cipher_blocks = [None] * len(msg_blocks)

    for m in range(0, len(msg_blocks)):
        # xor prev ciphertext block
        if m == 0:
            xor_block = xor(msg_blocks[m], iv)
        else:
            xor_block = xor(msg_blocks[m], cipher_blocks[m-1])
        # use block cipher
        cipher_blocks[m] = cipher.encrypt(xor_block)

    return b''.join(cipher_blocks)

def decrypt_aes_cbc(ciphertext, key, iv):
    # break plaintext into chunks
    cipher_blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
    cipher_blocks[len(cipher_blocks) - 1] = cipher_blocks[len(cipher_blocks) - 1] + \
                                      b''.join([b'0' for i in range(0, 16 - len(cipher_blocks[len(cipher_blocks) - 1]))])

    # set up block cipher
    cipher = AES.new(key, AES.MODE_ECB)

    # initialize encrypted blocks
    msg_blocks = [None] * len(cipher_blocks)

    for m in range(0, len(cipher_blocks)):
        # use block cipher FIRST this time
        msg_blocks[m] = cipher.decrypt(cipher_blocks[m])

        # then xor prev CIPHERTEXT block
        if m == 0:
            msg_blocks[m] = xor(msg_blocks[m], iv)
        else:
            msg_blocks[m] = xor(msg_blocks[m], cipher_blocks[m - 1])

    return b''.join(msg_blocks)

if __name__ == '__main__':
    ciphertext  = open("./s02_c10_input.txt", "r").read().replace('\n', '')
    plaintext = decrypt_aes_cbc(base64.b64decode(ciphertext), b'YELLOW SUBMARINE', b'\x00'*16)

