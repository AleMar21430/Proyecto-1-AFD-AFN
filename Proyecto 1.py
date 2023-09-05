from graphviz import Digraph
from Shunting import *
from STT import *
from NFA import *
from DFA import *

def nfa_to_dfa(nfa_i: NFA, nfa_f: NFA):
	sub_conjuntos = {}
	transiciones = []
	simbolos_entrada = extract_simbolos_entrada(nfa_i)
	s0 = epsilon_closure([nfa_i])
	sub_conjuntos["s0"] = [afn_node.label for afn_node in s0]
	s,t = subset(simbolos_entrada,sub_conjuntos, transiciones,["s0",s0])
	return build_dfa(s,t,nfa_f.label)

expr = "aabb"
infix_expr = "a|b*"

#expr = input("Cadena w:  ")
#expr = input("Expresión regular r:  ")

postfix_expr = infix_to_postfix(infix_expr)
print(f"Infix:   {infix_expr}")
print(f"Postfix: {postfix_expr}")

stt = build_stt(postfix_expr)
nfa_i, nfa_f = build_nfa(stt)
dfa = nfa_to_dfa(nfa_i, nfa_f)
#afn = Postfix_to_AFN(postfix_expr)
#dfa = AFN_to_AFD(afn)
#graph = Digraph(f"AFN",format='png')
#drawTree(graph, afn)
#graph = Digraph(f"AFD",format='png')
#drawTree(graph, dfa)
#graph.view()
print(f"La Cadena w: {expr} pertenece a {infix_expr}     w ∈ L(r) AFN: {simulate_nfa((nfa_i, nfa_f),expr)}")
print(f"La Cadena w: {expr} pertenece a {infix_expr}     w ∈ L(r) AFD: {simulate_dfa(dfa, expr)}")
