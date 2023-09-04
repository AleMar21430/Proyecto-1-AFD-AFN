

def infix_to_postfix(infix_expr):
	precedence = {
		".": 0,
		"+": 0,
		"-": 0,
		"/": 1,
		"*": 1,
		"|": 1,
		"!": 2,
		"^": 2
	}

	output = []
	stack = []

	for char in infix_expr:
		if char.isalpha():
			output.append(char)
		elif char == '(':
			stack.append(char)
		elif char == ')':
			while stack and stack[-1] != '(':
				output.append(stack.pop())
			stack.pop()
		else:
			while stack and precedence[char] <= precedence.get(stack[-1], 0):
				output.append(stack.pop())
			stack.append(char)

	while stack:
		output.append(stack.pop())

	return ''.join(output)