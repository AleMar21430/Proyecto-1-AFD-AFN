from graphviz import Digraph
from typing import Tuple, List
from STT import STT

class NFA:
	state = 0
	def __init__(self):
		self.label = f"q{self.state}"
		self.transitions = {}
		self.state += 1

	def add_transition(self, input: str, state):
		if input not in self.transitions: self.transitions[input] = set()
		self.transitions[input].add(state)

def epsilon_closure(states: List[NFA]) -> List[NFA]:
	new_states = states.copy()
	temp = set()

	while new_states:
		state = new_states.pop()
		if state not in temp:
			temp.add(state)
			if "ε" in state.transitions:
				new_states.extend(state.transitions["ε"])

	return list(temp)

def build_nfa(Node: STT) -> Tuple[NFA, NFA]:
	ei = NFA()
	ef = NFA()
	if not Node: return None, None

	if Node.value in ["*", ".", "|"]:
		if Node.value == "|":
			eiL, efL = build_nfa(Node.L)
			eiR, efR = build_nfa(Node.R)
			ei.add_transition("ε", eiL)
			ei.add_transition("ε", eiR)
			efL.add_transition("ε", ef)
			efR.add_transition("ε", ef)
		elif Node.value == "*":
			transitiveI, transitiveF = build_nfa(Node.R)
			ei.add_transition("ε", ef)
			ei.add_transition("ε", transitiveI)
			transitiveF.add_transition("ε",transitiveI)
			transitiveF.add_transition("ε",ef)

		elif Node.value == ".":
			eiL, efL = build_nfa(Node.L)
			eiR, efR = build_nfa(Node.R)
			ei = eiL
			ef = efR
			efL.add_transition("ε", eiR)
	else: ei.add_transition(Node.value, ef)

	return ei, ef

def visualize_nfa(root: NFA, end):
	dot = Digraph(format="png")
	dot.attr(rankdir="LR")
	visited = set()
	dot.node("_start", shape="point")
	dot.edge("_start", root.label, label="ε")
	visualize_nfa_node(dot, root, visited, end)
	return dot

def visualize_nfa_node(dot: Digraph, state: NFA , visited, end):
	if state:
		if state in visited:
			return

		visited.add(state)

		if state.label == end :
			dot.node(state.label, label=state.label, shape="doublecircle")
		else:
			dot.node(state.label, label=state.label, shape="circle")

		for i, nodes in state.transitions.items():
			for node in nodes:
				dot.edge(state.label, node.label, label=i)

		for i, nodes in state.transitions.items():
			for node in nodes:
				visualize_nfa_node(dot, node, visited,end)

def simulate_nfa(afn: Tuple[NFA, NFA], string: str):
	states = [afn[0]]
	states = epsilon_closure([afn[0]])

	for char in string:
		new_states = []
		for state in states:
			if char in state.transitions:
				new_states.extend(state.transitions[char])
		states = epsilon_closure(new_states)

	for state in states:
		if state.label == afn[1].label:
			return True

	return False