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
        return 'ECB', EncryptAES(plain, key)
    else:
        # CBC mode
        return 'CBC', encrypt_aes_cbc(plain, key, rand_key(16))


def detect_mode(ciphertext):
    # count repetitions of 16-byte blocks
    reps = count_repetitions(ciphertext, 16)
    # if there are any, call it ECB
    if sum(reps.values()) - len(reps) > 0:
        return 'ECB'
    else:
        return 'CBC'


# write a function to detect the mode
    # ECB mode has that plainblock -> cipherblock property
    # might be enough to say ECB or not ECB

if __name__ == "__main__":
    # is it OK to use a trivial string of one repeated char?
    # i peeked at other people's solutions and they did but it seems cheap and unrealistic
    plaintext = b'0'*16*4
    out = ['None'] * 1000
    for i in range(len(out)):
        ciphertext = hiddencrypt(plaintext, rand_key(16))
        out[i] = ciphertext[0] == detect_mode(ciphertext[1])
    print('trivial test message:', sum(out)/len(out))

    # not great for an actual message
    plaintext = open("./test_your_rump.txt", "r").read().replace('\n', '').encode('ascii')
    out = ['None'] * 100
    for i in range(len(out)):
        ciphertext = hiddencrypt(plaintext, rand_key(16))
        out[i] = ciphertext[0] == detect_mode(ciphertext[1])
    print('real test message:', sum(out) / len(out))
