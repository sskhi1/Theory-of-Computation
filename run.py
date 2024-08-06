accept_states_list = []
transition_table = {}


def check(current_states):
    for state in current_states:
        if state in accept_states_list:
            return True
    return False


def simulate_nfa(check_str):
    result = ""
    current_states = [0]
    for ch in check_str:
        next_states = [int(stt) for state in current_states
                       for stt in transition_table.get(state, {}).get(ch, [])]
        current_states = next_states
        result += 'Y' if check(current_states) else 'N'
    return result


def main():
    check_string = input()
    states_info = input()
    accept_states = input()
    n_str, a_str, t_str = states_info.split(' ')
    n = int(n_str)
    a = int(a_str)
    t = int(t_str)
    accept_states_list_str = accept_states.split(' ')
    for state in accept_states_list_str:
        accept_states_list.append(int(state))
    assert a == len(accept_states_list)
    num_transitions = 0
    for i in range(n):
        state_idx = i
        transition_table[state_idx] = {}
        state_transitions = input()
        state_transitions_list = state_transitions.split(' ')
        num_moves = int(state_transitions_list[0])
        moves = state_transitions_list[1:]
        num_transitions += num_moves
        for j in range(num_moves):
            symbol = moves[2 * j]
            state = moves[2 * j + 1]
            if symbol in transition_table[state_idx]:
                transition_table[state_idx][symbol].append(state)
            else:
                lst = [state]
                transition_table[state_idx][symbol] = lst
    for state_k in transition_table:
        for symbol in transition_table[state_k]:
            transition_table[state_k][symbol] = tuple(transition_table[state_k][symbol])
    assert t == num_transitions
    result = simulate_nfa(check_string)
    print(result)


if __name__ == '__main__':
    main()
