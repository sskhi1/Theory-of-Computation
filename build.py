class Transition:
    def __init__(self, symbol, idx):
        self.symbol = symbol
        self.state = idx

    def __eq__(self, other):
        return isinstance(other, Transition) and other.symbol == self.symbol and other.state == self.state

    def __hash__(self):
        return hash((self.symbol, self.state))


class NFA:
    def __init__(self, n, a, t, start_state, accept_states, transitions):
        self.n = n
        self.a = a
        self.t = t
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def is_accept_state(self, state):
        if state in self.accept_states:
            return True
        return False


def is_operand(ch):
    return ch.isalpha() or ch.isdigit() or ch == '#'


def regex_to_postfix(regex):
    precedence = {'*': 3, '.': 2, '|': 1, '(': 0}
    stk = []
    result = ''
    for ch in regex:
        if is_operand(ch) or ch == '*':
            result += ch
        elif ch == '(':
            stk.append(ch)
        elif ch == ')':
            while stk[-1] != '(' and len(stk) != 0:
                result += stk.pop()
            stk.pop()
        else:
            while len(stk) > 0 and stk[-1] != '(' and precedence[stk[-1]] >= precedence[ch]:
                result += stk.pop()
            stk.append(ch)
    while len(stk) > 0:
        result += stk.pop()
    return result


def insert_concatenation(regex):
    result = []
    for i in range(len(regex)):
        c = regex[i]
        result.append(c)
        if c in {'(', '|'}:
            continue
        if i < len(regex) - 1:
            next_c = regex[i + 1]
            if next_c in {'*', ')', '|'}:
                continue
            result.append('.')
    return ''.join(result)


def symbol_nfa(ch):
    transition = Transition(ch, 1)
    if transition.symbol == '#':
        nfa = NFA(1, 1, 0, 0, [0], [[]])
    else:
        nfa = NFA(2, 1, 1, 0, [1], [[transition], []])
    return nfa


def concat_nfa(nfa1, nfa2):
    n = nfa1.n + nfa2.n - 1
    a = nfa2.a
    t = nfa1.t + nfa2.t - len(nfa2.transitions[0])
    accept_states = [(nfa1.n + nfa2.accept_states[i] - 1) for i in range(nfa2.a)]
    transitions = [nfa1.transitions[i][:] for i in range(nfa1.n)] + \
                  [[Transition(t.symbol, t.state + nfa1.n - 1) for t in nfa2.transitions[i]] for i in range(1, nfa2.n)]
    for a_state in nfa1.accept_states:
        for tr in nfa2.transitions[0]:
            transitions[a_state].append(Transition(tr.symbol, nfa1.n + tr.state - 1))
            t += 1
    return NFA(n, a, t, 0, accept_states, transitions)


def union_nfa(nfa1, nfa2):
    n = nfa1.n + nfa2.n - 1
    a = nfa1.a + nfa2.a
    t = nfa1.t + nfa2.t
    accept_states = []
    transitions = [[]]
    if nfa1.is_accept_state(0) or nfa2.is_accept_state(0):
        accept_states.append(0)
    for tr in nfa1.transitions[0]:
        transitions[0].append(tr)
    for tr in nfa2.transitions[0]:
        transitions[0].append(Transition(tr.symbol, nfa1.n + tr.state - 1))
    for state in range(1, nfa1.n):
        if nfa1.is_accept_state(state):
            accept_states.append(state)
            trans = nfa1.transitions[state]
            lst = []
            for tr in trans:
                lst.append(Transition(tr.symbol, tr.state))
            transitions.append(lst)
        else:
            trans = nfa1.transitions[state]
            lst = []
            for tr in trans:
                lst.append(Transition(tr.symbol, tr.state))
            transitions.append(lst)
    for state in range(1, nfa2.n):
        if nfa2.is_accept_state(state):
            accept_states.append(nfa1.n + state - 1)
            trans = nfa2.transitions[state]
            lst = []
            for tr in trans:
                lst.append(Transition(tr.symbol, nfa1.n + tr.state - 1))
            transitions.append(lst)
        else:
            trans = nfa2.transitions[state]
            lst = []
            for tr in trans:
                lst.append(Transition(tr.symbol, nfa1.n + tr.state - 1))
            transitions.append(lst)
    return NFA(n, a, t, 0, accept_states, transitions)


def star_nfa(nfa1):
    n = nfa1.n + 2
    a = 1
    t = nfa1.t + nfa1.a * 2 + 2
    accept_states = [n - 1]
    transitions = [[Transition('#', 1), Transition('#', n - 1)]]
    for state in range(nfa1.n):
        if nfa1.is_accept_state(state):
            trans = nfa1.transitions[state]
            lst = []
            for tr in trans:
                lst.append(Transition(tr.symbol, tr.state + 1))
            lst.append(Transition('#', 1))
            lst.append(Transition('#', n - 1))
            transitions.append(lst)
        else:
            trans = nfa1.transitions[state]
            lst = []
            for tr in trans:
                lst.append(Transition(tr.symbol, tr.state + 1))
            transitions.append(lst)
    transitions.append([])
    return NFA(n, a, t, 0, accept_states, transitions)


def find_nfa(reg_exp):
    stk = []
    for ch in reg_exp:
        if is_operand(ch):
            stk.append(symbol_nfa(ch))
        elif ch == '.':
            nfa2 = stk.pop()
            nfa1 = stk.pop()
            stk.append(concat_nfa(nfa1, nfa2))
        elif ch == '*':
            nfa1 = stk.pop()
            stk.append(star_nfa(nfa1))
        elif ch == '|':
            nfa2 = stk.pop()
            nfa1 = stk.pop()
            stk.append(union_nfa(nfa1, nfa2))
    return stk.pop()


def get_epsilon_closure(n, i, visited, result):
    if visited[i]:
        return
    visited[i] = True
    for it in n.transitions[i]:
        if it.symbol == '#':
            to = it.state
            result.add(to)
            get_epsilon_closure(n, to, visited, result)


def remove_epsilon_transitions(nfa, i):
    visited = [False] * nfa.n
    epsilon_closure = set()
    epsilon_closure.clear()
    get_epsilon_closure(nfa, i, visited, epsilon_closure)
    for tr in nfa.transitions[i][:]:
        if tr.symbol == '#':
            nfa.transitions[i].remove(tr)

    for it in epsilon_closure:
        if nfa.is_accept_state(it):
            nfa.accept_states.append(i)
            nfa.accept_states = list(dict.fromkeys(nfa.accept_states))
        for it2 in nfa.transitions[it]:
            if it == i:
                continue
            if it2.symbol != '#':
                nfa.transitions[i].append(Transition(it2.symbol, it2.state))
                nfa.transitions[i] = list(dict.fromkeys(nfa.transitions[i]))


def remove_epsilons(nfa):
    for i in range(nfa.n):
        remove_epsilon_transitions(nfa, i)
    unreachable = [True] * nfa.n
    unreachable[0] = False
    for i in range(nfa.n):
        tran = nfa.transitions[i]
        for t in tran:
            if t.state < len(unreachable):
                unreachable[t.state] = False
    for i in range(len(unreachable) - 1, 0, -1):
        if unreachable[i]:
            nfa.n -= 1
            nfa.transitions.pop(i)
            if i in nfa.accept_states:
                nfa.accept_states.remove(i)
                for k in range(len(nfa.accept_states)):
                    if nfa.accept_states[k] > i:
                        nfa.accept_states[k] -= 1
            else:
                for k in range(len(nfa.accept_states)):
                    if nfa.accept_states[k] > i:
                        nfa.accept_states[k] -= 1

            for j in range(nfa.n):
                trans = nfa.transitions[j]
                updated = []
                for t in trans:
                    if t.state > i:
                        t.state = t.state - 1
                    updated.append(t)
                updated = list(dict.fromkeys(updated))
                nfa.transitions[j] = updated


def main():
    reg_exp = input()
    reg_exp = reg_exp.replace('()', '#')
    reg_exp = insert_concatenation(reg_exp)
    postfix_regexp = regex_to_postfix(reg_exp)
    print(postfix_regexp)
    nfa = find_nfa(postfix_regexp)
    remove_epsilons(nfa)
    nfa.a = len(nfa.accept_states)
    nfa.t = 0
    for i in range(len(nfa.transitions)):
        nfa.t += len(nfa.transitions[i])
    print(nfa.n, nfa.a, nfa.t)
    accepts = ''
    for state in nfa.accept_states:
        accepts += str(state) + ' '
    print(accepts)
    for i in range(len(nfa.transitions)):
        if len(nfa.transitions[i]) == 0:
            print('0')
        else:
            result = str(len(nfa.transitions[i])) + ' '
            for j in range(len(nfa.transitions[i])):
                transition = nfa.transitions[i][j]
                result += transition.symbol + ' ' + str(transition.state) + ' '
            print(result)


if __name__ == '__main__':
    main()
