from graphviz import Digraph
from typing import List, Dict, Set, Tuple
from NFA import NFA

class DFA:
	def __init__(self, name: str, accept: bool = False):
		self.label = name
		self.transitions = {}
		self.accept = accept

	def add_transition(self, input: str, state):
		self.transitions[input] = state

def epsilon_closure(afn_nodes: List[NFA], input: str = None) -> List[DFA]:
	new_states = afn_nodes.copy()
	visited = set()
	while new_states:
		state = new_states.pop()
		if state not in visited:
			visited.add(state)
			if input is not None and input in state.transitions:
				new_states.extend(state.transitions[input])
			if "ε" in state.transitions:
				new_states.extend(state.transitions["ε"])
			else:
				if "ε" in state.transitions:
					new_states.extend(state.transitions["ε"])
	return list(visited)

def build_dfa(states: Dict, transitions: Dict, final_state: DFA):
	AFD_states: List[DFA] = []
	for sub, states in states.items():
		if final_state in states:
			AFD_states.append(DFA(sub,True))
		else:
			AFD_states.append(DFA(sub))
	for transition in transitions:
		for state in AFD_states:
			if state.label == transition[1]:
				for destino in AFD_states:
					if destino.label == transition[2]:
						state.add_transition(transition[0], destino)
	return AFD_states[0]

def visualize_dfa(root: DFA):
	dot = Digraph("DFA", format="png")
	dot.attr(rankdir="LR")
	visited = set()
	dot.node("_start", shape="point")
	dot.edge("_start", root.label,)
	visualize_dfa_node(dot, root ,visited)
	return dot

def visualize_dfa_node(dot: Digraph, state: DFA , visited: DFA):
	if state:
		if state in visited: return
		visited.add(state)

		if state.accept: dot.node(state.label, label=state.label, shape="doublecircle")
		else: dot.node(state.label, label=state.label, shape="circle")

		for i, node in state.transitions.items(): dot.edge(state.label, node.label, label=i)
		for i, node in state.transitions.items(): visualize_dfa_node(dot, node, visited)

def simulate_dfa(dfa: Tuple[DFA, DFA], string: str) -> bool:
	return False

def extract_simbolos_entrada(afn_node: NFA, io: Set = set(), visited = []):
	if afn_node and afn_node.label not in visited:
		visited.append(afn_node.label)
		for s in afn_node.transitions:
			if s != "ε" and s not in io:
				io.add(s)
			for state in afn_node.transitions[s]:
				extract_simbolos_entrada(state,io)
	return io

def subset(symbols: str, subsets: Dict, transitions: List, subset_f, subset_i = 1) -> Tuple[Dict, List]:
	last_subset = subsets.copy()
	view_subset = []
	temp_subset = []

	for symbol in symbols:
		cerradura = epsilon_closure(subset_f[1], symbol)
		closure = [nfa_node.label for nfa_node in cerradura]
		if set(closure) not in [set(sub) for sub in subsets.values()]:
			name = f"s{subset_i}"
			subsets[name] = closure
			if [symbol, subset_f[0], name] not in transitions:
				transitions.append([symbol, subset_f[0] ,name])
			subsets[f"s{subset_i}"] = closure
			subset_i += 1
		else:
			for key, value in subsets.items():
				if set(value) == set(closure):
					result =  key
					if [symbol, result, result] not in transitions:
						transitions.append([symbol, result, result])
		view_subset.append(closure)
		temp_subset.append(cerradura)

	hits = 0
	for sub_observer in view_subset:
		for sub_last in last_subset.values():
			if len(sub_last) == len(sub_observer):
				if set(sorted(sub_last)) == set(sorted(sub_observer)):
					hits +=1 
	if hits < len(view_subset):
		for sub in temp_subset:
			subset(symbols,subsets,transitions,[f"s{subset_i-(len(temp_subset)-1)+temp_subset.index(sub)}",sub],subset_i)
	return subsets, transitions