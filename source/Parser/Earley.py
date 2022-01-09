VERTICAL_SYMBOL = "│"
VERTICAL_FORK = "├"
HORIZONTAL_SYMBOL = "─"
LEFT_SYMBOL = "└"
LEVEL_INDENT = 2

GAMMA_RULE = u"GAMMA"


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

    def add(self, term):
        self.terms += (term,)


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
    def __init__(self, name, production, dot_index, start_column, parent=None):
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]
        self.children = []
        self.parent = parent

    def __repr__(self):
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"·")
        return "%-5s -> %-16s [%s-%s]" % (self.name, " ".join(terms), self.start_column, self.end_column)

    def __eq__(self, other):
        return (self.name, self.production, self.dot_index, self.start_column) == \
               (other.name, other.production, other.dot_index, other.start_column)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.name, self.production))

    def __len__(self):
        return len(str(self))

    def completed(self):
        return self.dot_index >= len(self.production)

    def next_term(self):
        if self.completed():
            return None
        return self.production[self.dot_index]

    def addChild(self, state):
        self.children.append(state)


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


class Earley:
    def __predict(self, col, rule, state):
        for prod in rule.productions:
            col.add(State(rule.name, prod, 0, col))
            state.addChild(col[-1])

    def __scan(self, col, state, token):
        if token != col.token:
            return

        col.add(State(state.name, state.production, state.dot_index + 1, state.start_column, state))
        state.addChild(col[-1])

    def __complete(self, col, state):
        if not state.completed():
            return
        for st in state.start_column:
            term = st.next_term()
            if not isinstance(term, Rule):
                continue
            if term.name == state.name:
                col.add(State(st.name, st.production, st.dot_index + 1, st.start_column, st if st.parent is None else st.parent))
                st.addChild(col[-1])


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
                        self.__predict(col, term, state)
                    elif i + 1 < len(table):
                        self.__scan(table[i + 1], state, term)

            # col.print_(completedOnly = True)

        # find gamma rule in last table column (otherwise fail)
        for st in table[-1]:
            if st.name == GAMMA_RULE and st.completed():
                self.printTable(table)
                return table
        else:
            raise ValueError("parsing failed")


    def printTable(self, table, type="ver"):
        maxRow = 0
        colNum = 0
        if type == "hor":
            for col in table:
                print("| %135s " % str(colNum).center(135), end="")
                colNum += 1
                if len(col.states) > maxRow:
                    maxRow = len(col.states)

            print("|", end="\n")

            for i in range(0, maxRow):
                for col in table:
                    if i >= len(col.states):
                        break
                    else:
                        print("| %135s " % str(col.states[i]).center(135), end="")

                print("|", end="\n")
        else:
            i = 0
            for col in table:
                print(HORIZONTAL_SYMBOL * 15, " E_{0} ".format(i), HORIZONTAL_SYMBOL * 15)
                for state in col.states:
                    print(str(state).ljust(len(str(state))))
                i += 1
                print()


class TreeBuilder:
    def __init__(self, table):
        self.table = table

    def build_tree(self):
        for state in self.table[-1]:
            if state.name == GAMMA_RULE and state.completed():
                return self.__reduce_node(self.table[0].states[0])
        else:
            raise ValueError("Invalid earley table")

    def __reduce_node(self, state):
        result = Node(state, [])
        for child in state.children:
            if not child.children:
                if state.name == child.name:
                    result.value = child
            else:
                newChild = self.__reduce_node(child)
                # result.children.append(newChild)
                if newChild.value.name == state.name:
                    result.value = newChild.value
                    for childItem in newChild.children:
                        result.children.append(childItem)
                else:
                    result.children.append(newChild)
        return result

    def printTree(self, tree):
        self.__printTreeHelper(tree)

    def __printTreeHelper(self, node, indent='', nodeType='init'):
        if nodeType == 'last':
            start_shape = LEFT_SYMBOL + HORIZONTAL_SYMBOL * LEVEL_INDENT
        elif nodeType == 'mid':
            start_shape = VERTICAL_FORK + HORIZONTAL_SYMBOL * LEVEL_INDENT
        else:
            start_shape = ''

        print('{0}{1}{2}'.format(indent, start_shape, node.value))
        nextIndent = '{0}{1}'.format(indent, VERTICAL_SYMBOL + ' ' * (len(start_shape) - 1) if nodeType == 'mid' else ' ' * len(start_shape))

        if len(node.children) != 0:
            if len(node.children) == 1:
                self.__printTreeHelper(node.children[0], nextIndent, 'last')
            else:
                for i in range(0, len(node.children) - 1):
                    self.__printTreeHelper(node.children[0], nextIndent, 'mid')

                self.__printTreeHelper(node.children[len(node.children) - 1], nextIndent, 'last')