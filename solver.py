#User can interact with this solver through the terminal and input info to get the best guess at each step
#Narrows the dictionary down to only valid solutions
#Best guess is based on entropy from current guess

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
            if guess[i] == word[i]:
                report += '2'
            elif guess[i] in word:
                report += '1'
            else:
                report += '0'
        # Increments occurrences of particular report in dictionary
        probs[report] += 1
    total = len(words)
    # Converts count of reports to probability of report
    for report in probs:
        probs[report] = probs[report] / total
    return probs

# Finds the best guess given a list of valid words
def best_guess(words):
    entropy = {}
    for guess in words:
        # Gets the probability of possible reports given a guess in the list of possible words
        probs = get_probs(guess, words)
        entropy[guess] = 0
        # Sums info gains from each report times the probability of that report occurring given current word bank
        for report in probs:
            info = -math.log2(probs[report])
            entropy[guess] += probs[report] * info
    # Returns the guess with the maximum entropy
    return max(entropy, key=entropy.get)












# Checks if a word could be the answer given the current word bank, most recent guess, and most recent report
def check_valid(guess, word, report):
    # The most recent guess should not be considered valid if it was not the answer
    if guess == word:
        return False
    # Iterates through characters in the guess
    for i in range(8):
        char = guess[i]

        # mult1 stores the number of times the current character appears in the guess up to this point
        mult1 = 0
        for j in range(i + 1):
            if guess[j] == char:
                mult1 += 1

        # If the report says the character is correct and in the correct spot, the word must have the same character in the same spot
        if report[i] == '2':
            if word[i] != guess[i]:
                return False

        # If the report says the character is correct and in the wrong spot, the word cannot have the same character in the same spot
        # The word must have at least as many of this character as have appeared in the guess up to this point
        # This is because 1's are assigned in order
        if report[i] == '1':
            if guess[i] == word[i]:
                return False
            if mult1 > word.count(char):
                return False

        # If the report says the character is incorrect, the word cannot have this character more than it has been given a 1 or 2 in the guess
        if report[i] == '0':
            mult2 = 0
            # Counts the number of times this char has been given a 1 or 2 in the guess report
            # This is equal to the number of times the char belongs in the word
            for j in range(8):
                if guess[j] == char:
                    if report[j] == '1' or report[j] == '2':
                        mult2 += 1
            if word.count(char) > mult2:
                return False
    return True


# Gets valid guesses given the valid word pool, most recent guess, and report for that guess
# From the perspective of a human playing the game (not simulated)
def get_valids_human(guess, words, report):
    valids = []
    # Simply checks if each word is valid using check_valid()
    for word in words:
        valid = check_valid(guess, word, report)
        if valid:
            valids.append(word)
    return valids


def human_main():
    final_answer = None
    counter = 1
    valids = dictionary
    guess = input(f'What was your {counter}st guess? ')
    while guess not in valids:
        print('Invalid input')
        guess = input(f'What was your {counter}st guess? ')
    report = input(f'What was the report given? ')
    invalid = False
    if len(report) != 8:
        invalid = True
    for char in report:
        if char not in ['0', '1', '2']:
            invalid = True
    while invalid:
        invalid = False
        report = input(f'What was the report given? ')
        if len(report) != 8:
            invalid = True
        for char in report:
            if char not in ['0', '1', '2']:
                invalid = True
    while report != '22222222':
        valids = get_valids_human(guess, valids, report)
        guess_suggestion = best_guess(valids)
        if len(valids) > 1:
            show_valids = input(f'I would suggest guessing {guess_suggestion}, but there are still {len(valids)} possible answers. Would you like them listed? ')
        else:
            show_valids = input(f'Welp, looks like there\'s only one possible answer remaining. Would you like me to tell you what it is? ')
            final_answer = valids[0]
        if show_valids in ['Yes', 'yes', 'Y', 'y']:
            for answer in valids:
                print(answer)
        counter += 1
        if final_answer:
            print(f'I hope you guessed {final_answer}! According to what you told me, that has to be it!')
            print(f'Congrats! You got it in {counter} tries!')
            return
        if counter == 2:
            guess = input(f'What was your {counter}nd guess? ')
        elif counter == 3:
            guess = input(f'What was your {counter}rd guess? ')
        else:
            guess = input(f'What was your {counter}th guess? ')
        while guess not in valids:
            print('Invalid input')
            guess = input(f'What was your {counter}st guess? ')
        report = input(f'What was the report given? ')
        invalid = False
        for char in report:
            if char not in ['0', '1', '2']:
                invalid = True
        while invalid:
            invalid = False
            report = input(f'What was the report given? ')
            for char in report:
                if char not in ['0', '1', '2']:
                    invalid = True
        if counter > 6 and report != '22222222':
            print('I\'m sorry. I have failed you.')
            return
    if counter > 1:
        print(f'Congrats! You got it in {counter} tries.')
        return
    else:
        print('lol nice cheats! You got it on your first try!')
        return


human_main()
