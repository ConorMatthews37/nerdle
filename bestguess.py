import getdict
import math
from collections import defaultdict

dictionary = getdict.get_dict()


# Gets the probability of a report showing up given a guess and a set of words
def get_probs(guess, words):
    probs = defaultdict(lambda: 0)
    # Generates a report for the guess given each word in the set
    for word in words:
        report = ''
        for i in range(8):
            mult = 0
            char = word[i]
            for j in range(i + 1):
                if guess[j] == char:
                    mult += 1
            if guess[i] == word[i]:
                report += '2'
            elif guess[i] in word and mult < word.count(char):
                report += '1'
            else:
                report += '0'
        probs[report] += 1
    total = len(words)
    # Converts count of reports to probability of report
    for report in probs:
        probs[report] = probs[report] / total
    return probs

# Returns a sorted dictionary of the best guess given a list of valid words
def best_guess(words):
    entropy = {}
    for guess in words:
        # Gets the probability of possible reports given a guess in the list of possible words
        probs = get_probs(guess)
        entropy[guess] = 0
        # Finds the entropy of the guess
        for report in probs:
            # Calculates the information gain from a report, then multiplies by the probability of getting that report
            # The smaller a pool is, the smaller the probability of getting that pool and the more information you gain
            # in the event you narrow words down to that pool
            info = -math.log2(probs[report])
            entropy[guess] += probs[report] * info
    info = dict(sorted(entropy.items(), key=lambda item: item[1], reverse=True))
    return info

guesses = best_guess(dictionary)
with open('info1deepnew.txt', 'w') as file:
    for guess in guesses:
        file.write(f'{guess}, {guesses[guess]}\n')
