"""
NFA Epsilon Transition Removal Program
This program removes epsilon (ε) transitions from an NFA.
"""

"""
made by: 
Mourad Mostafa Saber group 1 IA
Moumen Mesbah  group 1  IA 

You might find us in the second group because the lists haven't been updated since we changed groups.
"""


def read_nfa():
    """
    Task 1: Read the NFA from user input
    Returns: dictionary containing NFA components
    """
    print("=== NFA Input ===")
    
    # Read number of states
    num_states = int(input("Enter number of states: "))
    states = list(range(num_states))
    
    # Read alphabet (without epsilon)
    alphabet_input = input("Enter alphabet symbols (space-separated, e.g., 'a b'): ")
    alphabet = alphabet_input.split()
    
    # Read initial state
    initial_state = int(input("Enter initial state: "))
    
    # Read final states
    final_input = input("Enter final states (space-separated): ")
    final_states = set(map(int, final_input.split()))
    
    # Read transitions
    print("\nEnter transitions (format: from_state symbol to_state)")
    print("Use 'epsilon' or 'e' for epsilon transitions")
    print("Enter 'done' when finished:")
    
    transitions = {}
    while True:
        trans = input("Transition: ").strip()
        if trans.lower() == 'done':
            break
        
        parts = trans.split()
        if len(parts) != 3:
            print("Invalid format. Use: from_state symbol to_state")
            continue
        
        from_state = int(parts[0])
        symbol = parts[1]
        to_state = int(parts[2])
        
        # Normalize epsilon representation
        if symbol.lower() in ['epsilon', 'e', 'ε']:
            symbol = 'ε'
        
        key = (from_state, symbol)
        if key not in transitions:
            transitions[key] = set()
        transitions[key].add(to_state)
    
    nfa = {
        'states': states,
        'alphabet': alphabet,
        'transitions': transitions,
        'initial_state': initial_state,
        'final_states': final_states
    }
    
    return nfa


def compute_epsilon_closure(state, transitions):
    """
    Task 2: Calculate the ε-closure of a given state
    ε-closure(q) = set of states reachable from q via ε-transitions (including q itself)
    """
    closure = {state}  # Include the state itself
    stack = [state]    # Stack for DFS
    
    while stack:
        current = stack.pop()
        
        # Check for epsilon transitions from current state
        key = (current, 'ε')
        if key in transitions:
            for next_state in transitions[key]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    
    return closure


def compute_all_epsilon_closures(states, transitions):
    """
    Compute epsilon closures for all states
    """
    epsilon_closures = {}
    for state in states:
        epsilon_closures[state] = compute_epsilon_closure(state, transitions)
    
    print("\n=== Epsilon Closures ===")
    for state in sorted(epsilon_closures.keys()):
        print(f"ε-closure({state}) = {sorted(epsilon_closures[state])}")
    
    return epsilon_closures


def compute_new_transitions(nfa, epsilon_closures):
    """
    Task 3: Compute new transitions without epsilon
    For each state q and symbol a:
    - Find all states reachable via ε-transitions from q
    - For each such state, find states reachable via 'a'
    - Compute ε-closure of those states
    """
    new_transitions = {}
    
    for state in nfa['states']:
        # Get epsilon closure of current state
        closure = epsilon_closures[state]
        
        # For each symbol in alphabet (not epsilon)
        for symbol in nfa['alphabet']:
            reachable = set()
            
            # For each state in the epsilon closure
            for s in closure:
                key = (s, symbol)
                if key in nfa['transitions']:
                    # Add states reachable via this symbol
                    for target in nfa['transitions'][key]:
                        # Add epsilon closure of target state
                        reachable.update(epsilon_closures[target])
            
            # Add transition if reachable set is not empty
            if reachable:
                new_transitions[(state, symbol)] = reachable
    
    return new_transitions


def compute_new_final_states(nfa, epsilon_closures):
    """
    Task 4: Determine new final states
    A state q is final if its ε-closure contains at least one original final state
    """
    new_final_states = set()
    
    for state in nfa['states']:
        closure = epsilon_closures[state]
        # Check if any state in closure is a final state
        if closure & nfa['final_states']:  # Set intersection
            new_final_states.add(state)
    
    return new_final_states


def display_new_automaton(nfa, new_transitions, new_final_states):
    """
    Task 5: Display the new automaton without epsilon transitions
    """
    print("\n" + "="*50)
    print("=== NFA WITHOUT EPSILON TRANSITIONS ===")
    print("="*50)
    
    print(f"\nStates: {nfa['states']}")
    print(f"Alphabet: {nfa['alphabet']}")
    print(f"Initial State: {nfa['initial_state']}")
    print(f"Final States: {sorted(new_final_states)}")
    
    print("\nTransitions:")
    print("-" * 40)
    for (from_state, symbol), to_states in sorted(new_transitions.items()):
        to_states_sorted = sorted(to_states)
        print(f"δ({from_state}, {symbol}) = {to_states_sorted}")
    
    print("\nTransition Table:")
    print("-" * 40)
    # Print header
    header = "State |"
    for symbol in nfa['alphabet']:
        header += f" {symbol:^8} |"
    print(header)
    print("-" * len(header))
    
    # Print transitions for each state
    for state in nfa['states']:
        row = f"  {state}   |"
        for symbol in nfa['alphabet']:
            key = (state, symbol)
            if key in new_transitions:
                targets = sorted(new_transitions[key])
                row += f" {str(targets):^8} |"
            else:
                row += f" {'-':^8} |"
        print(row)
    
    print("\n" + "="*50)


def main():
    """
    Main function to orchestrate the epsilon removal process
    """
    print("="*50)
    print("NFA EPSILON TRANSITION REMOVAL")
    print("="*50)
    
    # Task 1: Read NFA
    nfa = read_nfa()
    
    # Task 2: Compute epsilon closures
    epsilon_closures = compute_all_epsilon_closures(nfa['states'], nfa['transitions'])
    
    # Task 3: Compute new transitions
    new_transitions = compute_new_transitions(nfa, epsilon_closures)
    
    # Task 4: Compute new final states
    new_final_states = compute_new_final_states(nfa, epsilon_closures)
    
    # Task 5: Display result
    display_new_automaton(nfa, new_transitions, new_final_states)


if __name__ == "__main__":
    main()

