from Earley import Node


class TreeBuilder:
    def build_trees(self, state):
        return self.__build_trees_helper([], state, len(state.rules) - 1, state.end_column)

    def __build_trees_helper(self, children, state, rule_index, end_column):
        if rule_index < 0:
            return [Node(state, children)]
        elif rule_index == 0:
            start_column = state.start_column
        else:
            start_column = None

        rule = state.rules[rule_index]
        outputs = []
        for st in end_column:
            if st is state:
                break
            if st is state or not st.completed() or st.name != rule.name:
                continue
            if start_column is not None and st.start_column != start_column:
                continue
            for sub_tree in self.build_trees(st):
                for node in self.__build_trees_helper([sub_tree] + children, state, rule_index - 1, st.start_column):
                    outputs.append(node)
        return outputs
