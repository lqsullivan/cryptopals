from s02_c09 import pad, unpad
from s02_c11 import rand_key
from random import randint
from base64 import b64decode
from Crypto.Cipher import AES

# Break ECB byte-by-byte
# now we control a string between the random prefix and the target

class ECBOracle:
    def __init__(self, b64_target):
        """make a key and a cipher when you create an instance, use it forever"""
        self._key = rand_key(16)
        self._prefix = rand_key(randint(0, 255))
        self._aes_cipher = AES.new(self._key, AES.MODE_ECB)
        self._b64_target = b64_target

    def make_text(self, insert):
        return pad(self._prefix +
                   insert.encode('ascii') +
                   b64decode(self._b64_target), 16)

    def encrypt(self, insert):
        return self._aes_cipher.encrypt(pad(self.make_text(insert), 16))

    def decrypt(self, ciphertext):
        return unpad(self._aes_cipher.decrypt(ciphertext))


if __name__ == "__main__":
    b64_secret = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A='
    cipher = ECBOracle(b64_secret)
    cipher.encrypt('a')

    # if we can find the prefix boundary it'll be the same as 12
    # do that by handing it messages of increasing size until we get 2
    # consecutive identical cipher blocks
    def find_prefix_size(cipher):
        for i in range(0, 255 + 16*2):
            out_cipher = cipher.encrypt('A'*i)
            for j in range(0, len(out_cipher) // 16 - 2):
                if out_cipher[16*j:16*(j+1)] == out_cipher[16*(j+1):16*(j+2)]:
                    return 16*j - (i - 32)

    prefix_size = find_prefix_size(cipher)

    # insert characters until the message pushes into a new block
    # 0---------------1---------------2---------------
    # <prefix><pad><message+pad>
    # <prefix><pad            ><message+pad          >
    def find_msg_size(cipher, prefix_size):
        null_size = len(cipher.encrypt(''))
        for i in range(16):
            if len(cipher.encrypt('A'*i)) == (null_size + 16):
                return null_size - prefix_size - (i - 1)

    msg_size = find_msg_size(cipher, prefix_size)

    # now we can break the message as normal
    # minimum pad to align message with block boundary
    # example
    # 0---------------1---------------2---------------3+-->
    # <prefix><pad   ><AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA?*****
    # <prefix><pad   ><AAAAAAAAAAAAAAAAAAAAAAAAAAAAA!?*****
    message = [''] * msg_size
    check_block = (prefix_size + msg_size) // 16
    for i in range(msg_size):
        pad_size = 16 - (prefix_size + msg_size)%16
        test_pad = 'A'*(pad_size + msg_size - (i + 1))
        # prefix with chars and known message so the last byte of a block is the first unknown byte
        true_ciphertext = cipher.encrypt(test_pad)[16*check_block:16*(check_block+1)]
        for b in range(256):
            # pad so first unknown character ends a block
            candidate_ciphertext = cipher.encrypt(test_pad + ''.join(message) + chr(b))[16*check_block:16*(check_block+1)]
            # block to compare
            if true_ciphertext == candidate_ciphertext:
                message[i] = chr(b)
                break

    print(''.join(message))
