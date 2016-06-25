from tokenizer import tokens
from symbols import Symbol


class Production:

    def __init__(self, nullable=False):
        self.body = []
        self.nullable = nullable
        self.first = set([])
        self.follow = set([])


class Solver:

    def __init__(self, lines):
        self.symbols = {}
        self.productions = []
        for p in [tokens(line) for line in lines]:
            production = Production()
            size = 0
            for attr, val in p:
                if val not in self.symbols:
                    self.symbols[val] = Symbol(val=val, attr=attr)
                    if attr == 'Terminal':
                        self.symbols[val].first.add(val)
                production.body.append(val)
                size += 1
            if size == 1:
                self.symbols[val].nullable = True
            self.productions.append(production)

    def solve_nullable(self):
        changed = True
        while changed:
            changed = False
            for production in self.productions:
                if not self.symbols[production.body[0]].nullable:
                    flag = True
                    for i in range(1, len(production.body)):
                        if not self.symbols[production.body[i]].nullable:
                            flag = False
                            break
                    if flag:
                        changed = True
                        self.symbols[production[0]].nullable = True
                        production.nullable = True

    def solve_first(self):
        changed = True
        while changed:
            changed = False
            for production in self.productions:
                for i in range(1, len(production.body)):
                    cur_sym = production.body[i]
                    if self.symbols[production.body[0]].first >= self.symbols[cur_sym].first:
                        pass
                    else:
                        self.symbols[production.body[0]].first |= self.symbols[cur_sym].first
                        changed = True
                    if not self.symbols[cur_sym].nullable:
                        break
        for production in self.productions:
            if len(production.body) == 1:
                production.nullable = True
            for i in range(1, len(production.body)):
                sym = production.body[i]
                production.first |= self.symbols[sym].first
                if not self.symbols[sym].nullable:
                    break

    def solve_follow(self):
        changed = True
        while changed:
            changed = False
            for production in self.productions:
                temp_set = self.symbols[production.body[0]].follow.copy()
                for i in range(len(production.body) - 1, 0, -1):
                    cur_sym = production.body[i]
                    if self.symbols[cur_sym].follow >= temp_set:
                        pass
                    else:
                        self.symbols[cur_sym].follow |= temp_set
                        changed = True
                    if not self.symbols[cur_sym].nullable:
                        temp_set = set([])
                    temp_set |= self.symbols[cur_sym].first

    def create_table(self):
        table = {}
        for production in self.productions:
            for sym in production.first:
                if self.symbols[sym].attr == 'Terminal':
                    table.setdefault(production.body[0], {})[sym] = production
            if production.nullable:
                for sym in self.symbols[production.body[0]].follow:
                    if self.symbols[sym].attr == 'Terminal':
                        table.setdefault(production.body[0], {})[sym] = production
        self.table = table

    def gramer_analyze(self):
        pass


def test(file):
    f = open(file)
    s = Solver(f.readlines())
    s.solve_nullable()
    s.solve_first()
    s.solve_follow()
    table = s.create_table()
    for v in s.symbols.values():
        print v.val, v.nullable, v.first, v.follow
    print '\n'
    for k, v in table.items():
        print k
        for sym, p in v.items():
            print sym
            print p.body
        print '\n'
    f.close()
