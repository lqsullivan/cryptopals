
# identify letter frequency from corpus
char_freq = {
    'a': 0.08200, 'b': 0.01500, 'c': 0.02800, 'd': 0.04300, 'e': 0.13000, 'f': 0.02200,
    'g': 0.02000, 'h': 0.06100, 'i': 0.07000, 'j': 0.00150, 'k': 0.07700, 'l': 0.04000,
    'm': 0.02400, 'n': 0.06700, 'o': 0.07500, 'p': 0.01900, 'q': 0.00095, 'r': 0.06000,
    's': 0.06300, 't': 0.09100, 'u': 0.02800, 'v': 0.00980, 'w': 0.02400, 'x': 0.00150,
    'y': 0.02000, 'z': 0.00074
}

def get_letter_freq(str):
    freq = {}

    # get counts
    for char in str:
        if char in freq.keys():
            freq[char] += 1
        else:
            freq[char] = 1

    # normalize
    total = sum(freq.values())
    freq = {key: val/total for key,val in freq.items()}

    return(freq)

def simple_diff(d1, d2):
    # difference in proportions
    dsub = {key: d1.get(key, 0) - d2.get(key, 0) for key in d1}

    return(sum(dsub.values()))

def single_byte_xor(bcipher, bkey):
    keystream = bkey * (bcipher.__len__()//8)
    return(xor(keystream, bcipher))

# brute force single character xor and compare to letter frequency
def brute_force_single_char_xor(bcipher, char_freq_measure, verbose = False):
    best_str = ""
    best_val = 100
    best_key = ""

    # byte corresponds to integer 0-255
    for i in range(0, 256):
        bkey = bin(i)[2:].rjust(8, '0')

        bdecrypt = single_byte_xor(bcipher, bkey)

        plaintext = bin_to_ascii(bdecrypt)

        # get char frequency
        measure = char_freq_measure(char_freq,
                                    get_letter_freq(plaintext))

        # compare to standard with some measure
        if measure < best_val:
            best_val = measure
            best_str = plaintext
            best_key = chr(i)
            if verbose:
                # use better string formatting from python3?
                print("key  :", best_key, "("+bkey+")")
                print("score:", measure)
                print("text :", plaintext, "\n")

    return(best_key)

# challenge ----
# don't get fancy with the measure, absolute value ruined its performance
# with short text like this is think it was tuned to work with a simple difference
if __name__ == '__main__':
    hcipher = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    key = brute_force_single_char_xor(hex_to_bin(hcipher), char_freq_measure=simple_diff, verbose=True)
    assert key == 'X'
    assert bin_to_ascii(single_byte_xor(hex_to_bin(hcipher), ascii_to_bin(key))) == "Cooking MC's like a pound of bacon"