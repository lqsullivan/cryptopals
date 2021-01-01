from s02_c12 import rand_key
from s01_c07 import EncryptAES, DecryptAES
# i don't get where this is going

input = 'foo=bar&baz=qux&zap=zazzle'


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

    def profile_for(self, email):
        # clean metacharacters, no shenannigans
        email = email.replace('=', '').replace('&', '')

        return (string_kv({"email": email, "uid": "10", "role": "user"}))

    def encrypt(self, plaintext):
        """encrypt using that key"""
        return EncryptAES(plaintext.encode('ascii'), self._key)

    def decrypt(self, ciphertext):
        return DecryptAES(ciphertext, self._key).decode('ascii').strip('0')


# generate a random AES key
# encrypt the profile under that key
# decrpyt the encoded profile and parse it

cipher = ECBOracle()

cipher.profile_for('test@aol.com')
cipher.encrypt(cipher.profile_for('test@aol.com'))

