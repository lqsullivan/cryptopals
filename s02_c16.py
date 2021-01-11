from s02_c10 import CBC


class CBCOracle(CBC):
    """
    subclass of CBC with encrypt overwritten

    """
    def prep_string(self, plaintext):
        plaintext = plaintext.replace(';', '').replace('=', '')
        return 'comment1=cooking%20MCs;userdata=' + plaintext + ';comment2=%20like%20a%20pound%20of%20bacon'

    def encrypt(self, plaintext):
        # overwrite the parent encrypt with a new one that prepares the string
        return super().encrypt(self.prep_string(plaintext))


cipher = CBCOracle(key='YELLOW SUBMARINE', iv='\x00'*16)
cipher.encrypt('asdf')
