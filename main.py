import sys

stack = []
words = {}

class WordBase:
    def run():
        pass

class BuiltinWord:
    fun = None

    def __init__(self, python_fun):
        self.fun = python_fun

    def run(self):
        self.fun()

def add_word(name, word):
    words[name] = word

def _word_add():
    stack.append(stack.pop() + stack.pop())
add_word('+', BuiltinWord(_word_add))

def _word_mul():
    return stack.append(stack.pop() * stack.pop())
add_word('*', BuiltinWord(_word_mul))

def _word_div():
    div = stack.pop()
    stack.append(stack.pop() / div)
add_word('/', BuiltinWord(_word_div))

def _word_print():
    print(stack.pop())
add_word('print', BuiltinWord(_word_print))

filename = sys.argv[1]
tokens = []
with open(filename, 'r') as script:
    for line in script:
        tokens += line.split()

for tok in tokens:
    if tok.isnumeric():
        stack.append(int(tok))
    else:
        words[tok].run()
