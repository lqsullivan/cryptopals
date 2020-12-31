from random import randint
from s01_c07 import EncryptAES, DecryptAES
from s01_c08 import count_repetitions
from s02_c10 import encrypt_aes_cbc, decrypt_aes_cbc

# ECB/CBC detection oracle

# generate random AES key (16 bytes)
def rand_key(n_bytes=16):
    return bytes([randint(0, 255) for i in range(n_bytes)])


def hiddencrypt(plaintext, key):
    # append bytes to plaintext
    plain = rand_key(randint(5, 10)) + plaintext + rand_key(randint(5, 10))

    if randint(0, 1) == 0:
        # ECB mode
        ciphertext = EncryptAES(plain, key)
    else:
        # CBC mode
        ciphertext = encrypt_aes_cbc(plain, key, rand_key(16))

    return ciphertext


def detect_mode(ciphertext):
    # count repetitions of 2-byte blocks
    reps = count_repetitions(ciphertext, 2)
    sum(reps.values()) - len(reps)
    if

    return mode


# write a function to detect the mode
    # ECB mode has that plainblock -> cipherblock property
    # might be enough to say ECB or not ECB

if __name__ == "__main__":
    # randomly encrypt a bunch, then record guesses and answers?
    plaintext = b'Now I rock a house party at the drop of a hat, yeah\nI beat a biter down with an aluminum bat '
    hiddencrypt(plaintext, key=rand_key(16))
