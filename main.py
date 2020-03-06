import sys

stack = []
words = {}

class BuiltinWord:
    fun = None

    def __init__(self, python_fun):
        self.fun = python_fun

    def run(self):
        self.fun()

class ProgramWord:
    tokens = []

    def __init__(self, toks):
        self.tokens = toks

    def run(self):
        for t in self.tokens:
            if t.isnumeric():
                stack.append(int(t))
            else:
                words[t].run()

def add_word(name, word): words[name] = word

def _word_add(): stack.append(stack.pop() + stack.pop())
add_word('+', BuiltinWord(_word_add))

def _word_mul(): stack.append(stack.pop() * stack.pop())
add_word('*', BuiltinWord(_word_mul))

def _word_div():
    div = stack.pop()
    stack.append(stack.pop() / div)
add_word('/', BuiltinWord(_word_div))

def _word_print(): print(stack.pop())
add_word('print', BuiltinWord(_word_print))

filename = sys.argv[1]
tokens = []
with open(filename, 'r') as script:
    for line in script:
        tokens += line.split()

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
            elif tok.isnumeric():
                stack.append(int(tok))
            else:
                words[tok].run()
    except StopIteration:
        break
