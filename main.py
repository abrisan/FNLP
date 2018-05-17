simple_grammar = '''S
S -> NP VP
NP -> Det N
VP -> eats
VP -> eates
Det -> the
N -> man
'''

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
        assert nonterminal[0].isupper()

        return [x[1] for x in self.productions if x[0] == nonterminal]


class RecursiveDescentRecognizer:
    def __init__(self, grammar):
        self.grammar = grammar
        self.expansions = {}
        self.parse_stack = []

    def register_expansions_for_stack_size(self, stack_size, expansions):
        self.expansions[stack_size] = expansions

    def get_expansions_for_stack_size(self):
        stack_size = len(self.parse_stack)
        if not len(self.expansions[stack_size]):
            return None
        to_return = self.expansions[stack_size][0]
        self.expansions[stack_size] = self.expansions[stack_size][1:]

        return to_return

    def expand_stack(self, expansion):
        init_size = len(self.parse_stack)
        self.parse_stack = self.parse_stack[:-1]
        for i in range(len(expansion)-1, -1, -1):
            self.parse_stack.append({
                'symbol': expansion[i],
                'bpoint': init_size
            })

            expansions = self.grammar.get_expansions(expansion[i]) if not self.is_terminal() else []

            self.register_expansions_for_stack_size(
                len(self.parse_stack),
                expansions
            )

    def backtrack(self):
        print('backtrack called')
        bpoint = self.parse_stack[-1]["bpoint"]

        self.parse_stack = self.parse_stack[:bpoint-1]

    def match(self, symbol):
        if self.parse_stack[-1]['symbol'][0].islower():
            if self.parse_stack[-1]['symbol'] == symbol:
                self.parse_stack.pop()
                return True
        return False

    def is_terminal(self):
        if not len(self.parse_stack):
            return False
        return self.parse_stack[-1]['symbol'][0].islower()

    def parse(self, string):
        self.parse_stack = []
        self.expansions = {}

        tokens = string.strip().split()
        token_idx = 0

        self.register_expansions_for_stack_size(
            0,
            self.grammar.get_expansions(self.grammar.start_symbol)
        )

        self.expand_stack(
            self.get_expansions_for_stack_size()
        )

        while token_idx < len(tokens):
            print('>> Token IDX is {} and parse_stack is \n{}\nexpansions are \n{}\n'.format(token_idx, self.parse_stack, self.expansions))
            if self.is_terminal():
                if self.match(tokens[token_idx]):
                    token_idx += 1
                else:
                    print('>Expansions are now {}'.format(self.expansions))
                    self.backtrack()
            else:
                next_expansions = self.get_expansions_for_stack_size()
                print('Expansions are now {}'.format(self.expansions))

                if not next_expansions:
                    if not len(self.parse_stack):
                        return False
                    self.backtrack()
                    continue
                else:
                    self.expand_stack(next_expansions)

        print('The final parse stack is {}'.format(self.parse_stack))

        return len(self.parse_stack) == 0






if __name__ == '__main__':
    gr = Grammar(simple_grammar)

    pr = RecursiveDescentRecognizer(gr)

    print('The Man Eats is{} a valid phrase'.format(
        '' if pr.parse("the man eates") else ' not'))