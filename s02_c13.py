from s02_c12 import rand_key
from s02_c09 import pad, unpad
from Crypto.Cipher import AES


def parse_kv(input):
    """
    turn kv string into dict
    :param input:
    :return:
    """
    attrs = input.split('&')

    stuff = {}
    for a in attrs:
        pair = a.split('=')
        stuff[pair[0]] = pair[1]

    return(stuff)


def string_kv(input):
    return '&'.join([k + '=' + v for k, v in input.items()])


# inspired by github user ricpacca, i'm gonna make a class for this
class ECBOracle:
    def __init__(self):
        """make a key when you create an instance, use it forever"""
        self._key = rand_key(16)
        self._aes_cipher = AES.new(self._key, AES.MODE_ECB)

    def profile_for(self, email):
        # clean metacharacters, no shenannigans
        email = email.replace('=', '').replace('&', '')

        return (string_kv({"email": email, "uid": "10", "role": "user"}))

    def encrypt(self, plaintext):
        """encrypt using that key"""
        return self._aes_cipher.encrypt(pad(plaintext.encode('ascii'), 16))
        # EncryptAES(plaintext.encode('ascii'), self._key)

    def decrypt(self, ciphertext):
        return unpad(self._aes_cipher.decrypt(ciphertext))

    def make_profile(self, email):
        return self.encrypt(self.profile_for(email))

    def parse_encrypted_profile(self, ciphertext):
        return parse_kv(self.decrypt(ciphertext).decode('ascii'))


if __name__ == "__main__":
    # using only make_profile and parse_encrypted profile, make an admin role
    cipher = ECBOracle()
    cipher.make_profile('testemail@aol.com')
    cipher.parse_encrypted_profile(cipher.make_profile('testemail@aol.com'))

    # find block boundaries (16)
    for i in range(1, 128):
        plaintext = 'A'*2*i + "this is a test message that's long enough to probably cross a block"
        ciphertext = cipher.encrypt(plaintext)
        if ciphertext[:i] == ciphertext[i:2*i]:
            print(i)

    # figure out padding scheme (maybe pkcs7?)
    # 1---------------2---------------3---------------4---------------5---------------
    # email=AAAAAAAAAAuser{\x0b * 12} AAAAAAAAAAA@aol.com&uid=10&role=user{unk padding}
    # if block 0 and 4 of the ciphertext are identical, we know the padding
    test_pkcs7 = cipher.make_profile('A'*10 + 'user' + '\x0c'*12 + 'A'*11 + '@aol.com')
    if test_pkcs7[16:32] == test_pkcs7[64:80]:
        print('PKCS#7 padding')

    # Get an encrypted with the admin suffix as a block
    # 1---------------2---------------3---------------4---------------
    # email=AAAAAAAAAAadmin{\x0b * 11} @aol.com&uid=10&role=user
    has_admin = cipher.make_profile('A'*10 + 'admin' + '\x0b'*11 + '@aol.com')

    # cut the admin block, paste into the last position of the other
    admin_cipher = test_pkcs7[0:4*16] + has_admin[16:32]

    # did it work?
    admin = cipher.parse_encrypted_profile(admin_cipher)
    admin['role']


