class DFA_State:
	def __init__(self, label):
		self.transitions = {}
		self.label = label
		self.accepting = False

class DFA:
	def __init__(self):
		self.states = []
		self.start_state = None
		self.accept_state = None

	def add_state(self, label, accepting=False):
		state = DFA_State(label)
		state.accepting = accepting
		self.states.append(state)
		return state

	def add_transition(self, state1, state2, symbol):
		if symbol not in state1.transitions:
			state1.transitions[symbol] = []
		state1.transitions[symbol].append(state2)

def build_nfa(postfix_expr):
	nfa_stack = []

	for char in postfix_expr:
		if char.isalpha():
			nfa = DFA()
			start = nfa.add_state(char)
			end = nfa.add_state(char, accepting=True)
			start.transitions[char] = [end]
			nfa.start_state = start
			nfa.accept_state = end
			nfa_stack.append(nfa)
		elif char == '|':
			nfa2 = nfa_stack.pop()
			nfa1 = nfa_stack.pop()
			nfa = DFA()
			start = nfa.add_state('start')
			end = nfa.add_state('end', accepting=True)
			start.transitions['ε'] = [nfa1.start_state, nfa2.start_state]
			nfa1.accept_state.transitions['ε'] = [end]
			nfa2.accept_state.transitions['ε'] = [end]
			nfa.start_state = start
			nfa.accept_state = end
			nfa_stack.append(nfa)
		elif char == '*':
			nfa1 = nfa_stack.pop()
			nfa = DFA()
			start = nfa.add_state('start')
			end = nfa.add_state('end', accepting=True)
			start.transitions['ε'] = [nfa1.start_state, end]
			nfa1.accept_state.transitions['ε'] = [nfa1.start_state, end]
			nfa.start_state = start
			nfa.accept_state = end
			nfa_stack.append(nfa)
		elif char == '.':
			nfa2 = nfa_stack.pop()
			nfa1 = nfa_stack.pop()
			nfa1.accept_state.accepting = False
			for state in nfa1.states:
				if state.transitions.get('ε'):
					state.transitions['ε'].append(nfa2.start_state)
				else:
					state.transitions['ε'] = [nfa2.start_state]
			nfa1.accept_state = nfa2.accept_state
			nfa_stack.append(nfa1)

	return nfa_stack.pop()

def simulate_nfa(nfa, input_string):
	current_states = [nfa.start_state]

	for char in input_string:
		next_states = []
		for state in current_states:
			if state.transitions.get(char):
				next_states.extend(state.transitions[char])
		current_states = next_states

	for state in current_states:
		if state.accepting:
			return True

	return False