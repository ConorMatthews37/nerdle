#I wanted to see how this performed so I made this to run a bunch of simulations

import getdict
import random
import math
from collections import defaultdict
dictionary = getdict.get_dict()

def get_probs(guess, words):
    probs = defaultdict(lambda: 0)
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
    total = len(words)
    for prob in probs:
        probs[prob] = probs[prob] / total
    return probs

def best_guess(words):
    info = {}
    for guess in words:
        probs = get_probs(guess, words)
        info[guess] = 0
        for pattern in probs:
            info[guess] += -probs[pattern] * math.log2(probs[pattern])
    return max(info, key=info.get)

def get_valids(guess, words, word_of_day):
    report = get_report(guess, word_of_day)
    valids = []
    for word in words:
        valid = check_valid(guess, word, report)
        if valid:
            valids.append(word)
    return valids

def check_valid(guess, word, report):
    if guess == word:
        return False
    for i in range(8):
        char = guess[i]
        mult1 = 0
        for j in range(i + 1):
            if guess[j] == char:
                mult1 += 1
        if report[i] == '2':
            if word[i] != guess[i]:
                return False
        if report[i] == '1':
            if guess[i] == word[i]:
                return False
            if mult1 > word.count(char):
                return False
        if report[i] == '0':
            mult2 = 0
            for j in range(8):
                if guess[j] == char:
                    if report[j] == '1' or report[j] == '2':
                        mult2 += 1
            if word.count(char) > mult2:
                return False
    return True


def get_report(guess, word_of_day):
    report = ''
    for i in range(8):
        mult = 0
        char = guess[i]
        for j in range(i + 1):
            if guess[j] == char:
                mult += 1
        if guess[i] == word_of_day[i]:
            report += '2'
        elif guess[i] in word_of_day and mult <= word_of_day.count(char):
            report += '1'
        else:
            report += '0'
    return report

def make_guess(words, word_of_day):
    guess = best_guess(words)
    valids = get_valids(guess, words, word_of_day)
    return guess, valids

def solve(word_of_day):
    valids = dictionary
    guess = '48-32=16'
    valids = get_valids(guess, valids, word_of_day)
    counter = 1
    while guess != word_of_day:
        counter += 1
        guess, valids = make_guess(valids, word_of_day)
    return counter

def sim_games(n_games):
    results = defaultdict(lambda: 0)
    for i in range(n_games):
        wod = random.choice(dictionary)
        guesses = solve(wod)
        results[guesses] += 1
    return results


print(sim_games(10000))
