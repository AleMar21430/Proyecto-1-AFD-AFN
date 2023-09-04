from graphviz import Digraph
from Shunting import *
from AFN import *

class Tree_Node:
	def __init__(self, val):
		self.value = val
		self.L: Tree_Node | None = None
		self.R: Tree_Node | None = None

	def __str__(self):
		if self.value.isalnum(): return f"{self.value}"
		else: return f"({self.value} {str(self.L)} {str(self.R)})"


def epsilon_closure(nfa_states: Tree_Node):
	epsilon_closure_set = set(nfa_states)
	stack = list(nfa_states)

	while stack:
		state: Tree_Node = stack.pop()
		if state.L is not None and state.L.value == 'epsilon':
			epsilon_closure_set.add(state.L)
			stack.append(state.L)
		if state.R is not None and state.R.value == 'epsilon':
			epsilon_closure_set.add(state.R)
			stack.append(state.R)

	return epsilon_closure_set

def move(states, symbol):
	move_states = set()
	for state in states:
		if state.L is not None and state.L.value == symbol:
			move_states.add(state.L)
		if state.R is not None and state.R.value == symbol:
			move_states.add(state.R)
	return move_states


def AFN_to_AFD(nfa_root: Tree_Node):
	nfa_root = nfa_root
	dfa_states = {}
	start_state = epsilon_closure({nfa_root})

	unprocessed_states = [start_state]
	alphabet = set()

	while unprocessed_states:
		nfa_states: Tree_Node = unprocessed_states.pop()
		nfa_states_frozen = frozenset(nfa_states)  # Convert to frozenset

		dfa_states[nfa_states_frozen] = {}  # Use frozenset as dictionary key
		
		for node in nfa_states:
			if node.value.isalnum() and node.value not in alphabet:
				alphabet.add(node.value)

		for symbol in alphabet:
			move_result = move(nfa_states, symbol)
			epsilon_closure_result = epsilon_closure(move_result)

			if frozenset(epsilon_closure_result) not in dfa_states:
				unprocessed_states.append(epsilon_closure_result)

			dfa_states[nfa_states_frozen][symbol] = frozenset(epsilon_closure_result)  # Use frozenset as dictionary key

	return dfa_states

def Postfix_to_AFN(expr) -> Tree_Node | None:
	Stack = []
	for Char in expr:
		if Char in ['*', '+', '?', '.' , '|']:
			Node = Tree_Node(Char)
			try:
				Node.R = Stack.pop()
			except: pass
			try:
				if Char != '*': Node.L = Stack.pop()
			except: pass
			Stack.append(Node)
		else:
			Node = Tree_Node(Char)
			Stack.append(Node)
	return Stack[0] if Stack else None

def drawTree(graph: Digraph, node: Tree_Node):
	if node:
		graph.node(str(id(node)), label=node.value)
		if node.R:
			graph.node(str(id(node.R)), label=node.R.value)
			graph.edge(str(id(node)), str(id(node.R)))
			drawTree(graph, node.R)
		if node.L:
			graph.node(str(id(node.L)), label=node.L.value)
			graph.edge(str(id(node)), str(id(node.L)))
			drawTree(graph, node.L)

def itemPrecenedce(item):
	if item=='(': return 1
	elif item=='|': return 2
	elif item=='.': return 3
	elif item=='?': return 4
	elif item=='*': return 4
	elif item=='+': return 4

def simplifyRegex(regex):
	while '+' in regex:
		index = regex.index('+')
		if regex[index-1] != ')': regex.replace(regex[index-1] + '+', regex[index-1] + regex[index-1] + '*')
		elif regex[index-1] == ')':
			interior = index -2
			Group = 0
			while (regex[interior] != '(' or Group != 0)and interior>= 0:
				if regex[interior] == ')': Group += 1
				elif regex[interior] == '(': Group -= 1
				interior -= 1
			if regex[interior] == '(' and Group==0:
				expression = regex[interior:index]
				regex = regex.replace(expression + '+', expression + expression + '*')
		break
	while '?' in regex:
		index = regex.index('?')
		if regex[index-1] != '(': regex.replace(regex[index-1] + '?',"("+ regex[index-1] + '|ε)')
		elif regex[index-1] == ')':
			interior = index -2
			Group = 0
			while (regex[interior] != '(' or Group != 0)and interior>= 0:
				if regex[interior] == ')': Group += 1
				elif  regex[interior] == '(': Group -= 1
				interior -= 1
			if regex[interior] == '(' and Group==0:
				expression = regex[interior:index]
				regex = regex.replace(expression + '?', '(' + expression + '|ε)')
		break
	return regex

def formatRegEx(regex):
	regex = simplifyRegex(regex)
	OPs = ['|','?','+','*']
	binOPs = ['|']
	Result = ''
	for i in range(len(regex)):
		c1 = regex[i]
		if i+1<len(regex):
			c2 = regex[i+1]
			if c1=='\\':
				c1+=c2
				if i+2<len(regex): c2 = regex[i+2]
				else: c2 = ''
			elif c1=='[':
				j = i+1
				while j < len(regex) and regex[j]!=']':
					c1+=regex[j]
					j+=1
				c1+=regex[j]
				i = j
				if i+1<len(regex): c2 = regex[i+1]
				else: c2 = ''
			Result+=c1
			if c2!='' and c1!='(' and c2!=')' and c2 not in OPs and c1 not in binOPs: Result+='.'
		else: Result+=c1
	return Result

def simulate_NFA(node: Tree_Node, string):
	if not node:
		return False
	
	if node.value.isalnum():
		if len(string) == 0:
			return False
		elif string[0] == node.value:
			return simulate_NFA(node.R, string[1:])
		else:
			return False
	else:
		if node.value == '.':
			for i in range(len(string) + 1):
				if simulate_NFA(node.L, string[:i]) and simulate_NFA(node.R, string[i:]):
					return True
			return False
		elif node.value == '|':
			return simulate_NFA(node.L, string) or simulate_NFA(node.R, string)
		elif node.value == '*':
			for i in range(len(string) + 1):
				if simulate_NFA(node.L, string[:i]) and simulate_NFA(node.R, string[i:]):
					return True
			return simulate_NFA(node.L, string)
		elif node.value == '+':
			return simulate_NFA(node.L, string) and simulate_NFA(node.R, string[1:])
		elif node.value == '?':
			return simulate_NFA(node.L, string) or simulate_NFA(node.R, string)

def simulate_DFA(node: Tree_Node, string):
	if not node:
		return False

expresion = "abb"#input("Cadena w:  ")
infix_expr = "(a|b)*abb"#input("Expresión regular r:  ")

postfix_expr = infix_to_postfix(infix_expr)
print(f"Postfix: {postfix_expr}")

nfa = build_nfa(postfix_expr)
result = simulate_nfa(nfa, expresion)
#afn = Postfix_to_AFN(postfix_expr)
#dfa = AFN_to_AFD(afn)
#graph = Digraph(f"AFN",format='png')
#drawTree(graph, afn)
#graph = Digraph(f"AFD",format='png')
#drawTree(graph, dfa)
#graph.view()
print(f"La Cadena w: {expresion} pertenece a {infix_expr}     w ∈ L(r) ? {result}")
