import re
cache = {}

'''
def get_exprs(length):
    if length in cache:
        return cache[length]
    nums = '0123456789'
    ops = '-+/*'

    prefix = [c for c in nums + ops]
    if length == 1:
        return [x for x in nums]  # Must end with a number
    exprs = []

    nxt = get_exprs(length - 1)

    for val in prefix:
        for n in nxt:
            if val in ops and n[0] in ops:  # rule out consecutive operators
                continue
            else:
                expr = val + n
            exprs.append(expr)

    cache[length] = exprs
    return cache[length]

double_operator = re.compile(r'.*[\+\-\*/]{2,}.*')
leading_zero = re.compile(r'(0.*)|(.*[\+\-\*/]0.*)')
end_operator = re.compile(r'.*[\+\-\*/]$|^[\+\-\*/]')

x=4/3
print(x.is_integer())
'''

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

'''
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
'''


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

print(check_valid('39*6=234', '9*26=234', '01122222'))