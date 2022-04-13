import re
cache = {}

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

def calc(num1, num2, op):
    if op == '+':
        return num1 + num2
    if op == '-':
        return num1 - num2
    if op == '*':
        return num1 * num2
    if op == '/':
        return num1 / num2

def evaluate(expr):
    digits = '1234567890'
    num = ''
    nums = []
    ops = []
    for char in expr:
        if char in digits:
            num += char
        else:
            nums.append(int(num))
            ops.append(char)
            num = ''
    nums.append(int(num))
    if len(ops) == 0:
        return nums[0]
    if len(ops) == 1:
        return calc(nums[0], nums[1], ops[0])
    else:
        if ops[1] in '*/' and ops[0] in '+-':
            return calc(nums[0], calc(nums[1], nums[2], ops[1]), ops[0])
        else:
            return calc(calc(nums[0], nums[1], ops[0]), nums[2], ops[1])



def get_dict():
    words = []
    double_operator = re.compile(r'.*[\+\-\*/]{2,}.*')
    leading_zero = re.compile(r'(0.*)|(.*[\+\-\*/]0.*)')
    end_operator = re.compile(r'.*[\+\-\*/]$|^[\+\-\*/]')
    for length in range(4,7):
        for expr in get_exprs(length):
            if double_operator.match(expr):
                continue
            if leading_zero.match(expr):
                continue
            if end_operator.match(expr):
                continue
            #check if expr evaluates to a word of length 8
            val = evaluate(expr)
            if type(val) == int or val.is_integer():
                pass
            else:
                continue
            if val < 0:
                continue
            word = expr+'='+str(int(val))
            if len(word) == 8:
                words.append(word)
    return words
