precedence = {
	"(" : 1,
	"|" : 2,
	"." : 3,
	"?" : 4,
	"*" : 4,
	"+" : 4
}

def reformat(regex: str):
	while "+" in regex:
		index = regex.index("+")
		if regex[index-1] != ")": regex = regex.replace(f"{regex[index-1]}+", f"{regex[index-1]}{regex[index-1]}*")
		elif regex[index-1] == ")":
			interior = index -2
			group = 0 
			while (regex[interior] != "(" or group != 0) and interior >= 0:
				if regex[interior] == ")": group += 1
				elif regex[interior] == "(": group -= 1
				interior -= 1
			if regex[interior] == "(" and group == 0:
				expr = regex[interior: index]
				regex = regex.replace(f"{expr}+", f"{expr}{expr}*")
	while "?" in regex:
		index = regex.index("?")
		if regex[index-1] != ")": regex = regex.replace(f"{regex[index-1]}?", f"({regex[index-1]}|ε)")
		elif regex[index-1] == ")":
			interior = index -2
			group = 0
			while (regex[interior] != "(" or group != 0) and interior >= 0:
				if regex[interior] == ")": group += 1
				elif regex[interior] == "(": group -= 1
				interior -= 1
			if regex[interior] == "(" and group == 0:
				expr = regex[interior:index]
				regex = regex.replace(f"{expr}?", f"({expr}|ε)")

	ops = ["|","?","+","*"]
	bin = ["|"]
	res = ""
	i = 0
	while i < len(regex):
		value_A = regex[i]
		if i + 1 < len(regex):
			value_B = regex[i + 1]
			if value_A=="\\":
				value_A+=value_B
				if i + 2 < len(regex): value_B = regex[i + 2]
				else: value_B = ""
				i += 1
			elif value_A=="[":
				j = i + 1
				while j < len(regex) and regex[j] != "]":
					value_A+=regex[j]
					j += 1
				value_A+=regex[j]
				i=j
				if i + 1 < len(regex): value_B = regex[i + 1]
				else: value_B = ""
			res += value_A
			if value_B != "" and value_A != "(" and value_B != ")" and value_B not in ops and value_A not in bin: res += "."
		else: res += value_A
		i += 1
	return res

def infix_to_postfix(infix_expr):
	result = ""
	ops = ["|","?","+","*","."]
	stack = []
	format = reformat(infix_expr)
	i = 0
	while i < len(format):
		c = format[i]
		if c=="(":
			stack.append(c)
		elif c==")":
			while stack[-1]!="(":
				result+=stack.pop()
			stack.pop()
		elif c in ops:
			while len(stack)>0:
				peekedChar = stack[-1]
				peekedCharPrecedence = precedence[peekedChar]
				currentCharPrecedence = precedence[c]
				if peekedCharPrecedence>=currentCharPrecedence:
					result+=stack.pop()
				else:
					break
			stack.append(c)
		elif c=="\\":
			if i+1<len(format):
				result+=format[i+1]
				i+=1
		else:
			result+=c
		i+=1    
	while len(stack)>0:
		result+=stack.pop()
	return result