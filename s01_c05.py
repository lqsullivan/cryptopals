from s01_c01 import *

def repeat_to_length(input, max_len):
    """
    should work on list or string
    :param input:
    :param max_len:
    :return:
    """
    return((input * (max_len // len(input) + 1))[:max_len])

def encrypt_repeating_key_xor(plaintext, key):
    # repeat key across ciphertext
    key_rep = repeat_to_length(key, len(plaintext))

    ciphertext = xor(ascii_to_bin(plaintext), ascii_to_bin(key_rep))

    return ciphertext

# challenge ----
if __name__ == '__main__':
    # the test
    test = encrypt_repeating_key_xor("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal",
                                     "ICE")
    assert bin_to_hex(test) ==\
        "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

    # encrypt something else!
    de_la_plaintext  = open("./de_la_test.txt", "r").read()
    de_la_ciphertext = hex_to_ascii(encrypt_repeating_key_xor(de_la_plaintext, "D.A.I.S.Y. Age"))

