from s01_c07 import xor
from s02_c09 import pad, unpad
from Crypto.Cipher import AES
from base64 import b64decode

# ECB mode: break plaintext into blocks, use the block cipher on each block
# CBC mode: break plaintext into blocks, xor with last ciphertext block, then apply block cipher


class CBC:
    def __init__(self, key, iv):
        self._key = key.encode('ascii')
        self._iv = iv.encode('ascii')
        self._aes_cipher = AES.new(self._key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        # break plaintext into chunks
        msg_blocks = [plaintext[i:i + 16] for i in range(0, len(plaintext), 16)]
        msg_blocks[len(msg_blocks) - 1] = pad(msg_blocks[len(msg_blocks) - 1], 16)

        # initialize encrypted blocks
        cipher_blocks = [None] * len(msg_blocks)

        for m in range(0, len(msg_blocks)):
            # xor prev ciphertext block
            if m == 0:
                xor_block = xor(msg_blocks[m], self._iv)
            else:
                xor_block = xor(msg_blocks[m], cipher_blocks[m - 1])
            # use block cipher
            cipher_blocks[m] = self._aes_cipher.encrypt(xor_block)

        return b''.join(cipher_blocks)

    def decrypt(self, ciphertext):
        # break plaintext into chunks
        cipher_blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

        # initialize encrypted blocks
        msg_blocks = [None] * len(cipher_blocks)

        for m in range(0, len(cipher_blocks)):
            # use block cipher FIRST this time
            msg_blocks[m] = self._aes_cipher.decrypt(cipher_blocks[m])

            # then xor prev CIPHERTEXT block
            if m == 0:
                msg_blocks[m] = xor(msg_blocks[m], self._iv)
            else:
                msg_blocks[m] = xor(msg_blocks[m], cipher_blocks[m - 1])

        msg_blocks[len(cipher_blocks) - 1] = unpad(msg_blocks[len(cipher_blocks) - 1])
        return b''.join(msg_blocks)


if __name__ == '__main__':
    cipher = CBC(key='YELLOW SUBMARINE', iv='\x00'*16)
    ciphertext  = open("./s02_c10_input.txt", "r").read().replace('\n', '')
    plaintext = cipher.decrypt(b64decode(ciphertext))

