class Production(object):
    def __init__(self, *terms):
        self.terms = terms

    def __len__(self):
        return len(self.terms)

    def __getitem__(self, index):
        return self.terms[index]

    def __iter__(self):
        return iter(self.terms)

    def __repr__(self):
        return " ".join(str(t) for t in self.terms)

    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.terms)


class Rule(object):
    def __init__(self, name, *productions: Production):
        self.name = name
        self.productions = list(productions)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))

    def add(self, *productions):
        self.productions.extend(productions)


class State(object):
    def __init__(self, name, production, dot_index, start_column):
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]

    def __repr__(self):
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"$")
        return "%-5s -> %-16s [%s-%s]" % (self.name, " ".join(terms), self.start_column, self.end_column)

    def __eq__(self, other):
        return (self.name, self.production, self.dot_index, self.start_column) == \
               (other.name, other.production, other.dot_index, other.start_column)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.name, self.production))

    def completed(self):
        return self.dot_index >= len(self.production)

    def next_term(self):
        if self.completed():
            return None
        return self.production[self.dot_index]


class Column(object):
    def __init__(self, index, token):
        self.index = index
        self.token = token
        self.states = []
        self._unique = set()

    def __str__(self):
        return str(self.index)

    def __len__(self):
        return len(self.states)

    def __iter__(self):
        return iter(self.states)

    def __getitem__(self, index):
        return self.states[index]

    def enumfrom(self, index):
        for i in range(index, len(self.states)):
            yield i, self.states[i]

    def add(self, state):
        if state not in self._unique:
            self._unique.add(state)
            state.end_column = self
            self.states.append(state)
            return True
        return False

    def print_(self, completedOnly=False):
        print("[%s] %r" % (self.index, self.token))
        print("=" * 35)
        for s in self.states:
            if completedOnly and not s.completed():
                continue
            print(repr(s))
        print()


class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def print_(self, level=0):
        print("│" + " " * level + " " + str(self.value))
        for child in self.children:
            child.print_(level + 1)


GAMMA_RULE = u"GAMMA"


class Earley:
    def __predict(self, col, rule):
        for prod in rule.productions:
            col.add(State(rule.name, prod, 0, col))

    def __scan(self, col, state, token):
        if token != col.token:
            return
        col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))

    def __complete(self, col, state):
        if not state.completed():
            return
        for st in state.start_column:
            term = st.next_term()
            if not isinstance(term, Rule):
                continue
            if term.name == state.name:
                col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))

    def parse(self, rule, text):
        table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]
        table[0].add(State(GAMMA_RULE, Production(rule), 0, table[0]))

        for i, col in enumerate(table):
            for state in col:
                if state.completed():
                    self.__complete(col, state)
                else:
                    term = state.next_term()
                    if isinstance(term, Rule):
                        self.__predict(col, term)
                    elif i + 1 < len(table):
                        self.__scan(table[i + 1], state, term)

            # col.print_(completedOnly = True)

        # find gamma rule in last table column (otherwise fail)
        for st in table[-1]:
            if st.name == GAMMA_RULE and st.completed():
                return st
        else:
            raise ValueError("parsing failed")