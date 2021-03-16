import math
from .expand import expand_game_node


def select_node(node):
	if node.parent is None: #root node
		expand_game_node(node) #expand node the first time before selection
	return uct(node)


def uct(node):
	c = 1.41421 # math.sqrt(2), C is a constant to adjust the amount of exploration and incorporates the sqrt(2) from the UCB1 formula
							#Ved ikke lige med den C her
	arg_max_n = -1.0
	node_to_select = node
	for n in node.explored_nodes:
		x = n.number_of_wins / n.number_of_visists
		uct = x + c * math.sqrt((math.log2(n.parent.number_of_visits)/n.number_of_visists))
		if uct > arg_max_n and not node_to_select.isLeaf:
			arg_max_n = uct
			node_to_select = n
	if node_to_select.action_space is None or node_to_select.action_space is not []:
		expand_game_node(node_to_select)
	else:
		select_node(node_to_select)


