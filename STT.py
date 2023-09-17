from graphviz import Digraph

class STT:
	def __init__(self, val):
		self.value = val
		self.L: STT | None = None
		self.R: STT | None = None

def build_syntax_tree(expr: str) -> STT:
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

def visualize_stt(node: STT):
	graph = Digraph("STT","","STT","Graph","png")
	visualize_stt_node(graph, node)
	return graph

def visualize_stt_node(graph: Digraph, node: STT):
	if node:
		graph.node(str(id(node)), label=node.value)
		if node.L:
			graph.node(str(id(node.L)), label=node.L.value)
			graph.edge(str(id(node)), str(id(node.L)))
			visualize_stt_node(graph, node.L)
		if node.R:
			graph.node(str(id(node.R)), label=node.R.value)
			graph.edge(str(id(node)), str(id(node.R)))
			visualize_stt_node(graph, node.R)