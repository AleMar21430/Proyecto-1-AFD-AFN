from Shunting import *
from STT import *
from NFA import *
from DFA import *

expr = input("Cadena w:  ")

for i, infix_expr in enumerate(open("./Expr.txt").readlines()):
	NFA.state = 0

	infix_expr = infix_expr.strip()
	postfix_expr = infix_to_postfix(infix_expr)
	syntax_tree = build_syntax_tree(postfix_expr)
	nfa_start, nfa_end = build_nfa(syntax_tree)
	dfa = nfa_to_dfa(nfa_start, nfa_end)

	print("\n-----------------------------Regex--------------------------------")
	print(f"Infix:   {infix_expr}")
	print(f"Postfix: {postfix_expr}")
	print("---------------------------Simulation-----------------------------")
	print(f"if {{  w = {expr}  &&  L(r) = {infix_expr}  }}:  w ∈ L(r) ? NFA: {simulate_nfa((nfa_start, nfa_end),expr)}")
	print(f"if {{  w = {expr}  &&  L(r) = {infix_expr}  }}:  w ∈ L(r) ? DFA: {simulate_dfa(dfa, expr)}")
	print("------------------------------------------------------------------\n")

	graph = visualize_stt(syntax_tree, f"STT {i}")
	graph.view()

	graph = visualize_nfa(nfa_start, nfa_end, f"NFA {i}")
	graph.view()

	graph = visualize_dfa(dfa, f"DFA {i}")
	graph.view()