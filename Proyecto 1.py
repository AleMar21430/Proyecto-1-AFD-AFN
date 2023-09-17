from Shunting import *
from STT import *
from NFA import *
from DFA import *

def nfa_to_dfa(nfa_i: NFA, nfa_f: NFA):
	sub_set = {}
	transitions = []
	entry = extract_simbolos_entrada(nfa_i)
	s0 = epsilon_closure([nfa_i])
	sub_set["s0"] = [afn_node.label for afn_node in s0]
	s,t = subset(entry,sub_set, transitions,["s0",s0])
	return build_dfa(s,t,nfa_f.label)

expr = "ab"
infix_expr = "(a|b)?+ab*abb"

#expr = input("Cadena w:  ")
#expr = input("Expresión regular r:  ")

postfix_expr = infix_to_postfix(infix_expr)
print(f"Infix:   {infix_expr}")
print(f"Postfix: {postfix_expr}")

syntax_tree = build_syntax_tree(postfix_expr)
nfa_start, nfa_end = build_nfa(syntax_tree)

dfa = nfa_to_dfa(nfa_start, nfa_end)

print(f"La Cadena w: {expr} pertenece a {infix_expr}  ?   w ∈ L(r) NFA: {simulate_nfa((nfa_start, nfa_end),expr)}")
print(f"La Cadena w: {expr} pertenece a {infix_expr}  ?   w ∈ L(r) DFA: {simulate_dfa(dfa, expr)}")

graph = visualize_stt(syntax_tree)
graph.view()

graph = visualize_nfa(nfa_start, nfa_end)
graph.view()

graph = visualize_dfa(dfa)
graph.view()