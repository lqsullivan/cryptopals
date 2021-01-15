from Crypto.Cipher import AES
from s02_c10 import CBC
from s02_c11 import rand_key


class CBCOracle(CBC):
    """
    subclass of CBC with encrypt overwritten

    """
    def __init__(self, key, iv):
        self._key = key
        self._iv = iv
        self._aes_cipher = AES.new(self._key, AES.MODE_ECB)

    def prep_string(self, plaintext):
        plaintext = plaintext.replace(';', '').replace('=', '')
        return 'comment1=cooking%20MCs;userdata=' + plaintext + ';comment2=%20like%20a%20pound%20of%20bacon'

    def encrypt(self, plaintext):
        # overwrite the parent encrypt with a new one that prepares the string
        return super().encrypt(self.prep_string(plaintext))

    def is_admin(self, ciphertext):
        parsed = dict()
        for key, value in [str.split('=') for str in self.decrypt(ciphertext).split(';')]:
            parsed[key] = value

        if 'admin' in parsed.keys() and parsed['admin'] == 'true':
            return True
        else:
            return False


if __name__ == '__main__':
    # test new class
    cipher = CBCOracle(key=b'YELLOW SUBMARINE', iv=b'\x00'*16)
    a = cipher.encrypt('asdf')
    cipher.decrypt(a)
    cipher.is_admin(a)

    # modify the ciphertext to introduce an 'admin=true' block

    # for CBC mode, 1-bit error in ciphertext block scrambles the block, 1 bit error in next block
    # because the current block is block ciphered, 1 bit changes the whole thing (assuming good diffusion)
    # the next block gets xor'd with the last ciphertext, so that 1 bit change makes the same 1-bit change

    # so...i want to make 1-bit changes to ciphertext blocks
    # then observe and lock the bits as the next block produces the message i want
    # also have to find block boundaries first and adjust the input accordingly
    # maybe i input user data as one block and try to get it to be '<16bitgibberish>AAAA;admin=true;'?
    cipher = CBCOracle
