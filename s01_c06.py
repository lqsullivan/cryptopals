from s01_c01 import block_string, b64_to_hex
from s01_c02 import xor
from s01_c03 import brute_force_single_char_xor
from s01_c05 import *


def hamming_dist(bstr1, bstr2):
    """
    compute the hamming distance between two strings
    :param bstr1:
    :param bstr2:
    :return:
    """
    # count the 1s in xor, those are different bits
    out = xor(bstr1, bstr2).count("1")
    return out

# starting from scratch ----------------------------------------
def abs_diff(d1, d2):
    # difference in proportions
    dsub = {key: abs(d1.get(key, 0) - d2.get(key, 0)) for key in d1}

    return sum(dsub.values())

# principle: since the n-byte key is repeatedly applied, every n-th byte uses
# the same single byte key. we can break these independently if we know the
# keysize. we can guess it by assuming blocks of the correct key size are more
# similar than blocks of the incorrect keysize (i don't have an intuition for
# this part though)

def list_order(list):
    out = sorted(range(len(list)), key=lambda k: list[k])
    return out

def guess_keysize(ciphertext):
    # initialize distances
    mean_dist = {}
    for keysize in range(2, 41):
        # get the first few keysize chunks of bytes
        blocks = block_string(ciphertext, n=keysize*8, type='front')[0:5]
        block_dist = 0
        # hamming dist of pairs of blocks
        for a in range(0, len(blocks)):
            for b in range(a + 1, len(blocks)):
                # mean hamming dist per character
                block_dist += hamming_dist(blocks[a], blocks[b])/keysize
        # mean over all up to 10 unique pairs
        mean_dist[keysize] = block_dist/(len(blocks) * (len(blocks)-1) // 2)

    # find smallest values
    key_guesses = [item[0] for item in sorted(mean_dist.items(), key = lambda x: x[1])[:4]]

    return key_guesses

def break_rep_key_xor(ciphertext):
    # guess the key size
    key_sizes = guess_keysize(ciphertext)

    text_scores = {}
    for keysize in key_sizes:
        # break the ciphertext into keysized blocks
        blocks = pad_blocks(block_string(ciphertext, n=keysize*8, type='front'), n=keysize*8, type='back', pad_char='0')
        block_bytes = [block_string(block, 8, 'front') for block in blocks]
        # rearrange into blocks of the i-th *byte* of every block and break those as single-char xor
        # can't pick the key on the freq of a single block, do them all first
        key_chars = ''
        for i in range(keysize):
            # transposed block
            trans_block = ''.join([block[i] for block in block_bytes])
            # single-char xor each block (cause that's what happens in a repeating key xor)
            key_chars += brute_force_single_char_xor(trans_block, char_freq_measure=abs_diff, verbose=False)
            # when the ratio of ciphertext to key size is low (<20) this gets weird
        # translate the message under that key guess
        plain = encrypt_repeating_key_xor(bin_to_ascii(ciphertext), key_chars)
        text_scores[key_chars] = abs_diff(char_freq, get_letter_freq(plain))

    # pick best plaintext
    return min(text_scores, key=text_scores.get)

if __name__ == '__main__':
    # the test
    assert hamming_dist(ascii_to_bin("this is a test"),
                        ascii_to_bin("wokka wokka!!!")) == 37
    c = open('s01_c06_input.txt').read().replace('\n', '')
    ciphertext = b64_to_bin(c)
    key_guess = break_rep_key_xor(ciphertext)
    plaintext = bin_to_ascii(encrypt_repeating_key_xor(bin_to_ascii(ciphertext), key_guess))
    # either there's a typo 'gmrls' or the key is slightly wrong. but close enough for me

    # maybe this is just bad on small messages cause there are so many keys that subtend a reasonable letter freq
    de_la_plaintext  = open("./de_la_test.txt", "r").read()
    ciphertext = encrypt_repeating_key_xor(de_la_plaintext, "this is the key i'm using")
    key_guess = break_rep_key_xor(ciphertext)
    plaintext = bin_to_ascii(encrypt_repeating_key_xor(bin_to_ascii(ciphertext), key_guess))
