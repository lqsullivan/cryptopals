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
        self._aes_cipher = AES.new(self._key, AES.MODE_ECB)
        self._b64_target = b64_target

    def make_text(self, insert):
        return pad(rand_key(randint(0, 255)) + \
                   insert.encode('ascii') + \
                   b64decode(self._b64_target), 16)

    def encrypt(self, insert):
        return self._aes_cipher.encrypt(pad(self.make_text(insert), 16))

    def decrypt(self, ciphertext):
        return unpad(self._aes_cipher.decrypt(ciphertext))


# identify block size
# put in bytes one at a time, count the number of identical bytes at the beginning?
def guess_block_size(secret_key):
    for i in range(1, 128):
        ciphertext = append_ECB(b'A'*2*i, secret_key)
        if ciphertext[:i] == ciphertext[i:2*i]:
            return i
    # prob needs a default return


if __name__ == "__main__":
    b64_secret = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A'
    cipher = ECBOracle(b64_secret)

    cipher.encrypt('a')