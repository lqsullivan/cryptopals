# detect AES in ECB mode
# since 16-byte chunks always encode the same way, if we assume the true
# plaintext has more repeated 4-hex blocks than the others, we can
# just count those and find the one with the most

def count_repetitions(input, n=4):
    blocks = [input[i:i+n] for i in range(0, len(input), n)]

    count = {}

    # get counts
    for b in blocks:
        if b in count.keys():
            count[b] += 1
        else:
            count[b] = 1

    return count


# read input
if __name__ == '__main__':
    ciphertexts = [text for text in open('s01_c08_input.txt').read().splitlines()]

    total_reps = [None] * len(ciphertexts)


    for i in range(len(ciphertexts)):
        reps = count_repetitions(ciphertexts[i], 2)
        total_reps[i] = sum(reps.values()) - len(reps)

    [print(i, j) for i, j in enumerate(total_reps) if j == max(total_reps)]