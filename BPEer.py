from collections import defaultdict


def learn_bpe(corpus, num_merges):
    regexes = [r for r in corpus.split('  ') if r]

    vocab = defaultdict(int)
    for regex in regexes:
        for j in range(len(regex) - 1):
            pair = (regex[j], regex[j + 1])
            vocab[pair] += 1

    merges = []
    for _ in range(num_merges):
        if not vocab:
            break

        best_pair = max(vocab, key=lambda x: vocab[x])
        merges.append(best_pair)

        merged = ''.join(best_pair)
        new_vocab = defaultdict(int)
        for pair, count in vocab.items():
            if pair == best_pair:
                continue
            new_pair = list(pair)
            if new_pair[0] == best_pair[0] and new_pair[1] == best_pair[1]:
                new_pair[0] = merged
                new_pair.pop(1)
            new_vocab[tuple(new_pair)] += count
        vocab = new_vocab

    return merges


def apply_bpe(text, merges):
    chars = ['<'] + list(text) + ['>']

    for merge in reversed(merges):
        merged = ''.join(merge)
        new_chars = []
        i = 0
        while i < len(chars) - 1:
            if (chars[i], chars[i + 1]) == merge:
                new_chars.append(merged)
                i += 2
            else:
                new_chars.append(chars[i])
                i += 1
        if i < len(chars):
            new_chars.append(chars[-1])
        chars = new_chars

    return chars


if __name__ == '__main__':
    with open('corpus.txt', 'r') as f:
        corpus = f.read()

    merges = learn_bpe(corpus, num_merges=50)
    print("Learned merges:", merges)

    result = apply_bpe("bcd", merges)
    print("BPE for 'bcd':", result)

# reference: https://www.geeksforgeeks.org/nlp/byte-pair-encoding-bpe-in-nlp/
