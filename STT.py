from graphviz import Digraph
from typing import Tuple, List

class STT:
	def __init__(self, val):
		self.value = val
		self.L: STT | None = None
		self.R: STT | None = None

def build_stt(expr: str) -> STT:
	Stack = []
	for char in expr:
		if char in ['*', '+', '?', '.' , '|']:
			Node = STT(char)
			Node.R =Stack.pop()
			if char != '*':
				Node.L = Stack.pop()
			Stack.append(Node)
		else:
			Node = STT(char)
			Stack.append(Node)
	return Stack[0] if Stack else None

def visualize_stt(nodo: STT):
	dot = Digraph(format='png')
	if nodo:
		dot.node(str(id(nodo)), label = nodo.value)
		if nodo.L:
			dot.node(str(id(nodo.L)), label=nodo.L.value)
			dot.edge(str(id(nodo)), str(id(nodo.L)))
			visualize_stt(dot, nodo.L)
		if nodo.R:
			dot.node(str(id(nodo.R)), label=nodo.R.value)
			dot.edge(str(id(nodo)), str(id(nodo.R)))
			visualize_stt(dot, nodo.R)