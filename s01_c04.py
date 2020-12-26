
# read input
ciphertexts = [hex_to_bin(text) for text in open('s01_c04_input.txt').read().splitlines()]

def detect_single_char_xor(ciphertexts):
    all_key   = [''] * ciphertexts.__len__()
    all_score = [100] * ciphertexts.__len__()
    all_text  = [''] * ciphertexts.__len__()

    best_key = ""
    best_score = 100
    best_text = ""
    # byte corresponds to integer 0-255
    for i in range(256):
        # pick a key
        key = bin(i)[2:].rjust(8, "0")

        # brute force them
        for j in range(ciphertexts.__len__()):
            decrypt = single_byte_xor(ciphertexts[j], key)

            plaintext = bin_to_ascii(decrypt)

            # get char frequency
            measure = char_freq_measure(char_freq,
                                        get_letter_freq(plaintext))

            # compare to standard with some measure
            if measure < all_score[j]:
                all_key[j]   = chr(i)
                all_score[j] = measure
                all_text[j]  = plaintext
            if measure < best_score:
                best_score = measure
                best_key   = chr(i)
                best_text  = plaintext
                print("which:", j)
                print("score:", best_score)
                print("key  :", best_key)
                print("text :", best_text, "\n")

    return(best_key)

# challenge ----
if __name__ == '__main__':
    assert detect_single_char_xor(ciphertexts) == '5'