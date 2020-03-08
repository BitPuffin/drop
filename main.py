import sys

# Program environment
stack = []
words = {}

class BuiltinWord:
    def __init__(self, python_fun):
        self.fun = python_fun

    def run(self):
        self.fun()

class ProgramWord:
    def __init__(self, toks):
        self.tokens = toks

    def run(self):
        for t in self.tokens:
            interpret_token(t)


def add_word(name, word): words[name] = word

## Define built in words

def _word_add(): stack.append(stack.pop() + stack.pop())
add_word('+', BuiltinWord(_word_add))

def _word_mul(): stack.append(stack.pop() * stack.pop())
add_word('*', BuiltinWord(_word_mul))

def _word_div():
    div = stack.pop()
    stack.append(stack.pop() / div)
add_word('/', BuiltinWord(_word_div))

def _word_eq(): stack.append(stack.pop() == stack.pop())
add_word('=', BuiltinWord(_word_eq))

def _word_less_than():
    b = stack.pop()
    a = stack.pop()
    stack.append(a < b)
add_word('<', BuiltinWord(_word_less_than))

def _word_less_or_eq():
    b = stack.pop()
    a = stack.pop()
    stack.append(a <= b)
add_word('<=', BuiltinWord(_word_less_or_eq))

def _word_greater_than():
    b = stack.pop()
    a = stack.pop()
    stack.append(a > b)
add_word('>', BuiltinWord(_word_greater_than))

def _word_greater_or_eq():
    b = stack.pop()
    a = stack.pop()
    stack.append(a >= b)
add_word('>=', BuiltinWord(_word_greater_or_eq))

def _word_print(): print(stack.pop())
add_word('print', BuiltinWord(_word_print))

## read script
filename = sys.argv[1]
tokens = []
with open(filename, 'r') as script:
    for line in script:
        tokens += line.split()

inside_if = False
if_is_false = False
inside_else = False

## Evaluate script
def interpret_token(t):
    global inside_if, if_is_false, inside_else
    if (inside_if or inside_else) and t == 'then':
        inside_if = inside_else = False
        return
    if inside_if:
        if t == 'else':
            inside_if = False
            inside_else = True
        elif not if_is_false:
            get_value_or_run(t)
    elif inside_else:
        if if_is_false:
            get_value_or_run(t)
        else:
            if t == 'else':
                inside_else = False
    else:
        get_value_or_run(t)

def get_value_or_run(t):
    if t.isnumeric():
        stack.append(int(t))
    else:
        words[t].run()

tokiter = iter(tokens)
worddef = False
new_word_name = None
new_word = []

while True:
    try:
        tok = next(tokiter)
        if worddef:
            if tok == ';':
                worddef = False
                add_word(new_word_name, ProgramWord(new_word))
            elif tok == ':':
                raise "Nested words not allowed"
            else:
                new_word.append(tok)
        else:
            if tok == ':':
                worddef = True
                new_word = []
                try:
                    new_word_name = next(tokiter)
                except StopIteration:
                    raise "Unterminated Word"
            elif tok == 'if':
                val = stack.pop()
                inside_if = True
                if_is_false = val == 0
            else:
                interpret_token(tok)
    except StopIteration:
        break
