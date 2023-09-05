from graphviz import Digraph
from typing import Tuple, List, Dict
from NFA import NFA

class DFA:
	def __init__(self, name: str, accept: bool = False):
		self.label = name
		self.transitions = {}
		self.accept = accept

	def add_transition(self, input: str, state):
		self.transitions[input] = state

def epsilon_closure(afn_nodes: List[NFA], entrada: str = None):
	pass

def build_dfa(states: Dict, transitions: Dict, final_state: DFA):
	pass