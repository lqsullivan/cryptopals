from s01_c07 import EncryptAES
from s02_c11 import rand_key, detect_mode
from base64 import b64decode
from Crypto.Cipher import AES
cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
plaintext = cipher.decrypt(cipherbytes)

# Break ECB byte-by-byte (with ability to encrypt arbitrary messages including prefixing the real one)

# set an unknown key
secret_key = rand_key(16)

# append an unknown specific string to some known message before encrypting
def append_ECB(message, secret_key):
    to_append = b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

    # this is blazing fast compared to mine, but mine made me feel accomplished
    #cipher = AES.new(secret_key, AES.MODE_ECB)
    #return cipher.encrypt(pad(message + to_append, 16))

    return EncryptAES(message + to_append, secret_key)


# identify block size
# put in bytes one at a time, count the number of identical bytes at the beginning?
def guess_block_size(secret_key):
    for i in range(1, 128):
        ciphertext = append_ECB(b'A'*2*i, secret_key)
        if ciphertext[:i] == ciphertext[i:2*i]:
            return i
    # prob needs a default return


if __name__ == "__main__":
    block_size = guess_block_size(secret_key)

    # detect ECB
    detect_mode(append_ECB(b'A'*64, secret_key))


    message = [b''] * len(append_ECB(b'', secret_key))
    # for char in message
    for i in range(len(message)):
        # prefix with chars and known message so the last byte of a block is the first unknown byte
        true_ciphertext = append_ECB(b'A'*(block_size - ((i+1) % block_size)), secret_key)[:((i+1) // block_size + 1) * block_size]
        for b in range(256):
            test_msg = b'A'*(block_size - ((i+1) % block_size)) + b''.join(message) + bytes([b])
            candidate_ciphertext = append_ECB(test_msg, secret_key)[:((i+1) // block_size + 1) * block_size]
            # carriage returns are new to me
            print(b''.join(message) + bytes([b]), end = '\r')
            if true_ciphertext == candidate_ciphertext:
                message[i] = bytes([b])
                break

    # is slow, but it works

