import re

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


class RegexpRule(object):
    def __init__(self, regexp):
        self.regexp = regexp

    def __repr__(self):
        return self.regexp


class State(object):
    def __init__(self, name, production, dot_index, start_column):
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]
        self.children = []

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
    def __init__(self, value, children, lexeme):
        self.state = value
        self.children = children
        self.lexeme = lexeme

    def __repr__(self):
        terms = [str(p) for p in self.state.production]
        terms.insert(self.state.dot_index, u"·")
        return "{0} -> {1}         Lexeme: {2}".format(self.state.name, " ".join(terms), self.lexeme)


class Earley:
    def __init__(self, rules, axiom):
        self.rules = rules
        self.axiom = None
        self.table = None

        for rule in rules:
            if rule.name == axiom:
                self.axiom = rule

        if self.axiom is None:
            raise ValueError("Invalid axiom")

    def __predict(self, col, rule, state):
        for prod in rule.productions:
            newState = State(rule.name, prod, 0, col)
            col.add(newState)
            state.addChild(newState)

    def __scan(self, col, state, token):
        if not isinstance(token, RegexpRule):
            if token == col.token.lexeme:
                col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))
                state.addChild(col[-1])
        else:
            match = re.search(token.regexp, col.token.lexeme)
            if match:
                col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))
                state.addChild(col[-1])

    def __complete(self, col, state):
        if not state.completed():
            return
        for st in state.start_column:
            term = st.next_term()
            if not isinstance(term, Rule):
                continue
            if term.name == state.name:
                col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))
                st.addChild(col[-1])

    def parse(self, lexemeArray):
        self.table = [Column(i, tok) for i, tok in enumerate([None] + lexemeArray)]
        self.table[0].add(State(GAMMA_RULE, Production(self.axiom), 0, self.table[0]))

        for i, col in enumerate(self.table):
            for state in col:
                if state.completed():
                    self.__complete(col, state)
                else:
                    term = state.next_term()
                    if isinstance(term, Rule):
                        self.__predict(col, term, state)
                    elif i + 1 < len(self.table):
                        self.__scan(self.table[i + 1], state, term)

            # col.print_(completedOnly = True)

        # find gamma rule in last table column (otherwise fail)
        for st in self.table[-1]:
            if st.name == GAMMA_RULE and st.completed():
                return True
        else:
            return False

    def printTable(self, type="ver"):
        maxRow = 0
        colNum = 0
        if type == "hor":
            for col in self.table:
                print("| %135s " % str(colNum).center(135), end="")
                colNum += 1
                if len(col.states) > maxRow:
                    maxRow = len(col.states)

            print("|", end="\n")

            for i in range(0, maxRow):
                for col in self.table:
                    if i >= len(col.states):
                        break
                    else:
                        print("| %135s " % str(col.states[i]).center(135), end="")

                print("|", end="\n")
        else:
            i = 0
            for col in self.table:
                print(HORIZONTAL_SYMBOL * 10, " E_{0} - token: {1}".format(i, col.token), HORIZONTAL_SYMBOL * 10)
                for state in col.states:
                    print(str(state).ljust(len(str(state))))
                i += 1
                print()


class TreeBuilder:
    def __init__(self, table):
        self.table = table
        self.tree = None
        self.file = None

    def build_tree_test(self, state):
        return self.build_tree_helper([], state, len(state.rules) - 1, state.end_column)

    def build_tree_helper(self, children, state, rule_index, end_column):
        if rule_index < 0:
            return [Node(state, children, state.start_column.token)]

        rule = state.rules[rule_index]
        outputs = []
        for col in self.table[::-1]:
            for st in col:
                if st is state:
                    break
                if not st.completed() and st.name != rule.name:
                    continue
                test = self.build_tree_test(st)
                for sub_tree in test:
                    outputs.append([sub_tree])
                if test:
                    break

        return outputs

    def build_tree(self):
        for state in self.table[-1]:
            if state.name == GAMMA_RULE and state.completed():
                # self.tree = self.table[0].states[0]
                self.tree = self.__reduce_node(self.table[0].states[0])
                return
        else:
            raise ValueError("Invalid earley table")

    def __reduce_node(self, state):
        if state.end_column:
            lexeme = state.end_column.token
        else:
            lexeme = None

        result = Node(state, [], lexeme)

        if not state.children:
            return result

        for child in state.children:
            child = self.__reduce_node(child)

            if child.state.name == state.name and child.state.production == state.production and child.state.completed():
                result.state = child.state
                result.lexeme = child.state.end_column.token
                result.children.extend(child.children)
            elif child.state.completed():
                if (child.state.rules and child.children) or not child.state.rules:
                    result.children.append(child)

        return result

    def printTreeToFile(self):
        if self.tree is not None:
            with open("Tree.txt", "w+", encoding="utf-8") as file:
                self.file = file
                self.__printTreeToFileHelper(self.tree)

    def printTreeToFileTest(self, trees):
        if trees is not None:
            with open("Tree1.txt", "w+", encoding="utf-8") as file:
                self.file = file
                for tree in trees:
                    self.__printTreeToFileHelper(tree)
                    self.file.write('\n')

    def __printTreeToFileHelper(self, current_node, indent='', nodeType='init', nameattr='value'):
        if hasattr(current_node, nameattr):
            name = getattr(current_node, nameattr)
        else:
            name = repr(current_node)

        if nodeType == 'last':
            start_shape = LEFT_SYMBOL + HORIZONTAL_SYMBOL * LEVEL_INDENT
        elif nodeType == 'mid':
            start_shape = VERTICAL_FORK + HORIZONTAL_SYMBOL * LEVEL_INDENT
        else:
            start_shape = ' '

        line = '{0}{1}{2}'.format(indent, start_shape, name)
        self.file.write(line + '\n')
        nextIndent = '{0}{1}'.format(indent, VERTICAL_SYMBOL + ' ' * (len(start_shape)) if nodeType == 'mid' else ' ' * (len(start_shape) + 1))

        if len(current_node.children) != 0:
            if len(current_node.children) == 1:
                self.__printTreeToFileHelper(current_node.children[0], nextIndent, 'last')
            else:
                for i in range(0, len(current_node.children) - 1):
                    self.__printTreeToFileHelper(current_node.children[i], nextIndent, 'mid')

                self.__printTreeToFileHelper(current_node.children[-1], nextIndent, 'last')

    def printTree(self):
        if self.tree is not None:
            self.__printTreeHelper(self.tree)

    def __printTreeHelper(self, node, indent='', nodeType='init'):
        if nodeType == 'last':
            start_shape = LEFT_SYMBOL + HORIZONTAL_SYMBOL * LEVEL_INDENT
        elif nodeType == 'mid':
            start_shape = VERTICAL_FORK + HORIZONTAL_SYMBOL * LEVEL_INDENT
        else:
            start_shape = ' '

        print('{0}{1}{2}'.format(indent, start_shape, node.state))
        nextIndent = '{0}{1}'.format(indent, VERTICAL_SYMBOL + ' ' * (len(start_shape)) if nodeType == 'mid' else ' ' * (len(start_shape) + 1))

        if len(node.children) != 0:
            if len(node.children) == 1:
                self.__printTreeHelper(node.children[0], nextIndent, 'last')
            else:
                for i in range(0, len(node.children) - 1):
                    self.__printTreeHelper(node.children[i], nextIndent, 'mid')

                self.__printTreeHelper(node.children[len(node.children) - 1], nextIndent, 'last')