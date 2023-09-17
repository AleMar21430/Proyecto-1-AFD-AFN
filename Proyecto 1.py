from Shunting import *
from STT import *
from NFA import *
from DFA import *

expr = "ab"
infix_expr = "(a|b)?+ab*abb"

#expr = input("Cadena w:  ")
#expr = input("Expresión regular r:  ")

postfix_expr = infix_to_postfix(infix_expr)

syntax_tree = build_syntax_tree(postfix_expr)
nfa_start, nfa_end = build_nfa(syntax_tree)
dfa = nfa_to_dfa(nfa_start, nfa_end)

print("\n-----------------------------Regex--------------------------------")
print(f"Infix:   {infix_expr}")
print(f"Postfix: {postfix_expr}")
print("---------------------------Simulation-----------------------------")
print(f"La Cadena w: {expr} pertenece a {infix_expr}  ?   w ∈ L(r) NFA: {simulate_nfa((nfa_start, nfa_end),expr)}")
print(f"La Cadena w: {expr} pertenece a {infix_expr}  ?   w ∈ L(r) DFA: {simulate_dfa(dfa, expr)}")
print("------------------------------------------------------------------\n")

graph = visualize_stt(syntax_tree)
graph.view()

graph = visualize_nfa(nfa_start, nfa_end)
graph.view()

graph = visualize_dfa(dfa)
graph.view()