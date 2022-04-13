import getdict
import itertools
import math
from collections import defaultdict
dictionary = getdict.get_dict()

def get_probs(guess, words):
    probs = defaultdict(lambda: 0)
    valids = defaultdict(lambda: [])
    for word in words:
        report = ''
        for i in range(8):
            if guess[i] == word[i]:
                report += '2'
            elif guess[i] in word:
                report += '1'
            else:
                report += '0'
        probs[report] += 1
        valids[report].append(word)
    total = len(words)
    for prob in probs:
        probs[prob] = probs[prob] / total
    return probs, valids

def best_guess2(words):
    total_info = defaultdict(lambda: 0)
    info1 = {}
    for guess1 in words:
        total_info[guess1] = 0
        info1[guess1] = 0
        info2 = {}
        probs1, valids1 = get_probs(guess1, dictionary)
        for pattern1 in probs1:
            info1[guess1] += -probs1[pattern1] * math.log2(probs1[pattern1])
        for pattern1 in valids1:
            prob_pattern = len(valids1[pattern1]) / len(dictionary)
            for guess2 in valids1[pattern1]:
                probs2, valids2 = get_probs(guess2, valids1[pattern1])
                info2[guess2] = 0
                for pattern2 in probs2:
                    info2[guess2] += -probs2[pattern2] * math.log2(probs2[pattern2])
            best_second_guess = max(info2, key=info2.get)
            total_info[guess1] += prob_pattern * (info1[guess1] + info2[best_second_guess])
        total_info = dict(sorted(total_info.items(), key=lambda item: item[1], reverse=True))
    return total_info

best_guesses = best_guess2(dictionary)
first5pairs = {k: best_guesses[k] for k in list(best_guesses)[:5]}
print(first5pairs)