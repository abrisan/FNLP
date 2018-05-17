simple_grammar = '''S
S -> NP VP
S -> N
NP -> Det N
VP -> eats
VP -> eates
Det -> the
N -> man
N -> abracadabra
'''

class Stack:
    def __init__(self):
        self.state = []

    def isEmpty(self):
        return len(self.state) == 0

    def push(self, element):
        self.state.append(element)

    def pop(self):
        element = self.peek()
        self.state.pop()
        return element

    def peek(self):
        return self.state[-1]

    def size(self):
        return len(self.state)

    def __str__(self):
        str_v = '['

        for elem in self.state:
            str_v += str(elem) + ','

        if (len(self.state)):
            str_v = str_v[:-1]

        str_v += ']'

        return str_v

class Grammar:
    def __init__(self, strg_value):
        self.raw_string = strg_value
        self.init_grammar()

    def init_grammar(self):
        split_lines = self.raw_string.strip().split('\n')
        self.start_symbol = split_lines[0]
        split_lines = [x.split('->') for x in split_lines[1:]]
        split_lines = [(x[0].strip(), x[1].strip().split()) for x in split_lines]
        self.productions = split_lines

    def get_expansions(self, nonterminal):
        ret_value = Stack()

        if nonterminal[0].islower():
            return ret_value

        for x in [y for y in self.productions if y[0] == nonterminal]:
            ret_value.push(x[1])

        return ret_value


class RecursiveDescentRecognizer:
    def __init__(self, grammar):
        self.grammar = grammar
        self.expansions = Stack()
        self.parse_stack = Stack()

    def expand_top_symbol(self, tokens_idx):
        top_symbol = self.parse_stack.peek()['symbol']

        if self.expansions.isEmpty() or self.expansions.peek().isEmpty():
            return False

        self.parse_stack.peek()['visited'] = True

        next_expansion = self.expansions.peek().pop()

        backtrack_point = len(next_expansion)

        for i, symbol in enumerate(reversed(next_expansion)):
            self.parse_stack.push({
                'symbol': symbol,
                'backtrack_to': i+1,
                'tokens_idx': tokens_idx,
                'visited': False
            })

            self.expansions.push(
                self.grammar.get_expansions(symbol)
            )

        return True

    def match(self, symbol):
        current_symbol = self.parse_stack.peek()['symbol']

        if current_symbol[0].isupper():
            return 'nonterminal'

        return 'match' if current_symbol == symbol else 'no match'

    def backtrack(self):
        n_elems_to_pop = self.parse_stack.peek()['backtrack_to']
        token_idx = self.parse_stack.peek()['tokens_idx']

        for i in range(n_elems_to_pop):
            self.parse_stack.pop()
            self.expansions.pop()

        return token_idx

    def parse(self, string):
        tokens = string.strip().split()

        token_idx = 0

        self.parse_stack.push({
            'symbol': self.grammar.start_symbol,
            'backtrack_to': 1,
            'visited': False,
            'tokens_idx': 0
        })

        self.expansions.push(
            self.grammar.get_expansions(self.grammar.start_symbol)
        )

        self.expand_top_symbol(token_idx)

        while token_idx < len(tokens):
            if self.parse_stack.isEmpty():
                return False

            match_try = self.match(tokens[token_idx])

            if match_try == 'nonterminal':
                if not self.expand_top_symbol(token_idx):
                    token_idx = self.backtrack()
            elif match_try == 'no match':
                token_idx = self.backtrack()
            else:
                token_idx += 1
                self.parse_stack.pop()
                self.expansions.pop()

                while not self.parse_stack.isEmpty() and self.parse_stack.peek()['visited']:
                    self.parse_stack.pop()
                    self.expansions.pop()

        return self.parse_stack.isEmpty()

if __name__ == '__main__':
    gr = Grammar(simple_grammar)

    pr = RecursiveDescentRecognizer(gr)

    print(pr.parse('abracadabra'))

