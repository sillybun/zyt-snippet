import re

def generate_matrix(prefix, snip):
	info = snip.buffer[snip.line]
	# print(info, snip.snippet_start, snip.snippet_end)
	spacelen = len(info) - len(info.lstrip())
	linfo = info[:snip.snippet_start[1]]
	rinfo = info[snip.snippet_end[1]:]
	info = info[snip.snippet_start[1]:snip.snippet_end[1]]
	# print([linfo, rinfo, info])
	if len(info) > 1 and info[1].isnumeric():
		real_shape = info[:2]
		virtual_shape = info[2:]
	else:
		real_shape = info[0]
		virtual_shape = info[1:]
	if len(real_shape) == 1:
		row_amount = int(real_shape)
		column_amount = int(real_shape)
	else:
		row_amount = int(real_shape[0])
		column_amount = int(real_shape[1])
	if len(virtual_shape) == 0:
		virtual_row_amount = "0"
		virtual_column_amount = "0"
	elif len(virtual_shape) == 1:
		virtual_row_amount = virtual_shape[0]
		virtual_column_amount = virtual_shape[0]
	else:
		virtual_row_amount = virtual_shape[0]
		virtual_column_amount = virtual_shape[1]
	# print(row_amount, column_amount, virtual_row_amount, virtual_column_amount)
	snip.buffer[snip.line] = ''
	displayed = linfo + "\\begin{%cmatrix}\n" % prefix
	def generate_code(i, j, row, column, virtual_row, virtual_column):
		code = """
`!p
vdot = False
hdot = False
i = %d
j = %d
row = %d
column = %d
virtual_row = "%c"
virtual_column = "%c"
if i > 1 and t[j].strip() == "\\\\cdots":
	vdot = True
if j > 1 and t[1 + column * (i - 1)].strip() == "\\\\vdots":
	hdot = True
if vdot and hdot:
	snip.rv = "\\\\ddots"
elif vdot:
	snip.rv = "\\\\cdots"
elif hdot:
	snip.rv = "\\\\vdots"
elif i > 1 or j > 1:
	if virtual_row == "0":
		if i > 1 and j > 1:
			value = ""
			if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]) == re.sub("\d", "*", t[1 + column]):
				for index in range(len(t[1])):
					if not t[1][index].isnumeric():
						value += t[1][index]
					else:
						x1 = int(t[1][index])
						x2 = int(t[2][index])
						x3 = int(t[1+column][index])
						value += str((x2 - x1) * (j-1) + (x3 - x1) * (i-1) + x1)
				snip.rv = value
			elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
				snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
			else:
				snip.rv = ""
		elif i > 2:
			value = ""
			if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[1 + column]):
				for index in range(len(t[1])):
					if not t[1][index].isnumeric():
						value += t[1][index]
					else:
						x1 = int(t[1][index])
						x3 = int(t[1+column][index])
						value += str((x3 - x1) * (i-1) + x1)
				snip.rv = value
			elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
				snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
			else:
				snip.rv = ""
		elif j > 2:
			value = ""
			if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]):
				for index in range(len(t[1])):
					if not t[1][index].isnumeric():
						value += t[1][index]
					else:
						x1 = int(t[1][index])
						x2 = int(t[2][index])
						value += str((x2 - x1) * (j-1) + x1)
				snip.rv = value
			elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
				snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
			else:
				snip.rv = ""
		elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
			snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
		else:
			snip.rv = ""
	else:
		vdot = False
		hdot = False
		if %s:
			hdot = True
		if %s:
			vdot = True
		flag = False
		if i > 1 and j > 1:
			value = ""
			if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]) == re.sub("\d", "*", t[1 + column]):
				for index in range(len(t[1])):
					if not t[1][index].isnumeric():
						value += t[1][index]
					else:
						x1 = int(t[1][index])
						x2 = int(t[2][index])
						x3 = int(t[1+column][index])
						virtual_bias = ""
						bias = x1
						if not vdot:
							bias += (x2 - x1) * (j - 1)
						else:
							bias += -(column - j) * (x2 - x1) - (x2 - x1)
							if x2 != x1:
								if x2 == x1 + 1:
									virtual_bias += virtual_column
								elif x1 == x2 + 1:
									virtual_bias += "-" + virtual_column
								else:
									virtual_bias += str(x2 - x1) + virtual_column
						if not hdot:
							bias += (x3 - x1) * (i - 1)
						else:
							bias += -(row - i) * (x3 - x1) - (x3 - x1)
							if x3 != x1:
								if x3 == x2 + 1:
									virtual_bias += ("+" if virtual_bias else "") + virtual_column
								elif x1 == x2 + 1:
									virtual_bias += "-" + virtual_column
								else:
									virtual_bias += ("+" if virtual_bias and x2 > x1 else "") + str(x2 - x1) + virtual_column
						if bias == 0:
							value += virtual_bias
						else:
							value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
				snip.rv = value
				flag = True
		elif i > 2:
			value = ""
			if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[1 + column]):
				for index in range(len(t[1])):
					if not t[1][index].isnumeric():
						value += t[1][index]
					else:
						x1 = int(t[1][index])
						x3 = int(t[1+column][index])
						virtual_bias = ""
						bias = x1
						if not hdot:
							bias += (x3 - x1) * (i - 1)
						else:
							bias += -(row - i) * (x3 - x1) - (x3 - x1)
							if x3 != x1:
								if x3 == x2 + 1:
									virtual_bias += ("+" if virtual_bias else "") + virtual_column
								elif x1 == x2 + 1:
									virtual_bias += "-" + virtual_column
								else:
									virtual_bias += ("+" if virtual_bias and x2 > x1 else "") + str(x2 - x1) + virtual_column
						if bias == 0:
							value += virtual_bias
						else:
							value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
				snip.rv = value
				flag = True
		elif j > 2:
			value = ""
			if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]):
				for index in range(len(t[1])):
					if not t[1][index].isnumeric():
						value += t[1][index]
					else:
						x1 = int(t[1][index])
						x2 = int(t[2][index])
						virtual_bias = ""
						bias = x1
						if not vdot:
							bias += (x2 - x1) * (j - 1)
						else:
							bias += -(column - j) * (x2 - x1) - (x2 - x1)
							if x2 != x1:
								if x2 == x1 + 1:
									virtual_bias += virtual_column
								elif x1 == x2 + 1:
									virtual_bias += "-" + virtual_column
								else:
									virtual_bias += str(x2 - x1) + virtual_column
						if bias == 0:
							value += virtual_bias
						else:
							value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
				snip.rv = value
				flag = True
		if not flag and re.match(".*[a-zA-Z]_\{11\}", t[1]):
			if not vdot and not hdot:
				snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
			elif vdot and hdot:
				snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", t[1])
			elif vdot:
				snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", t[1])
			else:
				snip.rv = re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + str(j) + "}", t[1])
		if not flag:
			snip.rv = ""
else:
	snip.rv = ""
`
""" % (i, j, row, column, virtual_row, virtual_column, " or ".join(["t[%d].strip() == '\\\\vdots'" % (1 + column * (x - 1)) for x in range(1, i)]) if i > 1 else "False", " or ".join(["t[%d].strip() == '\\\\cdots'" % x for x in range(1, j)]) if j > 1 else "False")
		# if i == 5 and j == 5:
		# 	print(code)
		return code[1:-1]
	if row_amount > 0 and column_amount > 0:
		displayed += " " * (4 + len(linfo)) + "$1\t" + ("& " if column_amount > 1 else "\\" * 4)
		index = 2
		for i in range(2, column_amount + 1):
			displayed += "${" + "{}".format(index) + ":" + "`!p\nimport sys\nsys.path.append('/Users/zhangyiteng/.vim/plugged/zyt-snippet/UltiSnips')\nfrom pythonutil import generate_matrix_element\nsnip.rv = generate_matrix_element(1, %d, %d, %d, '%c', '%c')`" % (i, row_amount, column_amount, virtual_row_amount, virtual_column_amount) + "}\t" + ("& " if i < column_amount else "\\" * 4)
			index += 1
		displayed += "\n"
		for j in range(2, row_amount + 1):
			displayed += " " * (4 + len(linfo))
			for i in range(1, column_amount + 1):
				displayed += "${" + "{}".format(index) + ":" + "`!p\nimport sys\nsys.path.append('/Users/zhangyiteng/.vim/plugged/zyt-snippet/UltiSnips')\nfrom pythonutil import generate_matrix_element\nsnip.rv = generate_matrix_element(%d, %d, %d, %d, '%c', '%c')`" % (j, i, row_amount, column_amount, virtual_row_amount, virtual_column_amount) + "}\t" + ("& " if i < column_amount else "\\" * 4)
				index += 1
			displayed += "\n"
	displayed += " " * len(linfo) + "\\end{%cmatrix}" % prefix + (" " + rinfo if rinfo else "")
	snip.expand_anon(displayed)

def generate_matrix_element(i, j, row, column, virtual_row, virtual_column):
	vdot = False
	hdot = False
	if i > 1 and t[j].strip() == "\\cdots":
		vdot = True
	if j > 1 and t[1 + column * (i - 1)].strip() == "\\vdots":
		hdot = True
	if vdot and hdot:
		return "\\ddots"
	elif vdot:
		return "\\cdots"
	elif hdot:
		return "\\vdots"
	elif i > 1 or j > 1:
		if virtual_row == "0":
			if i > 1 and j > 1:
				value = ""
				if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]) == re.sub("\d", "*", t[1 + column]):
					for index in range(len(t[1])):
						if not t[1][index].isnumeric():
							value += t[1][index]
						else:
							x1 = int(t[1][index])
							x2 = int(t[2][index])
							x3 = int(t[1+column][index])
							value += str((x2 - x1) * (j-1) + (x3 - x1) * (i-1) + x1)
					return value
				elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
					return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
				else:
					return ""
			elif i > 2:
				value = ""
				if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[1 + column]):
					for index in range(len(t[1])):
						if not t[1][index].isnumeric():
							value += t[1][index]
						else:
							x1 = int(t[1][index])
							x3 = int(t[1+column][index])
							value += str((x3 - x1) * (i-1) + x1)
					return value
				elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
					return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
				else:
					return ""
			elif j > 2:
				value = ""
				if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]):
					for index in range(len(t[1])):
						if not t[1][index].isnumeric():
							value += t[1][index]
						else:
							x1 = int(t[1][index])
							x2 = int(t[2][index])
							value += str((x2 - x1) * (j-1) + x1)
					return value
				elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
					return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
				else:
					return ""
			elif re.match(".*[a-zA-Z]_\{11\}", t[1]):
				return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
			else:
				return ""
		else:
			vdot = False
			hdot = False
			if any(t[1 + (x-1) * column] == "\\vdots" for x in range(i)):
				hdot = True
			if any(t[x] == "\\cdots" for x in range(j)):
				vdot = True
			flag = False
			if i > 1 and j > 1:
				value = ""
				if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]) == re.sub("\d", "*", t[1 + column]):
					for index in range(len(t[1])):
						if not t[1][index].isnumeric():
							value += t[1][index]
						else:
							x1 = int(t[1][index])
							x2 = int(t[2][index])
							x3 = int(t[1+column][index])
							virtual_bias = ""
							bias = x1
							if not vdot:
								bias += (x2 - x1) * (j - 1)
							else:
								bias += -(column - j) * (x2 - x1) - (x2 - x1)
								if x2 != x1:
									if x2 == x1 + 1:
										virtual_bias += virtual_column
									elif x1 == x2 + 1:
										virtual_bias += "-" + virtual_column
									else:
										virtual_bias += str(x2 - x1) + virtual_column
							if not hdot:
								bias += (x3 - x1) * (i - 1)
							else:
								bias += -(row - i) * (x3 - x1) - (x3 - x1)
								if x3 != x1:
									if x3 == x2 + 1:
										virtual_bias += ("+" if virtual_bias else "") + virtual_column
									elif x1 == x2 + 1:
										virtual_bias += "-" + virtual_column
									else:
										virtual_bias += ("+" if virtual_bias and x2 > x1 else "") + str(x2 - x1) + virtual_column
							if bias == 0:
								value += virtual_bias
							else:
								value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
					return value
					flag = True
			elif i > 2:
				value = ""
				if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[1 + column]):
					for index in range(len(t[1])):
						if not t[1][index].isnumeric():
							value += t[1][index]
						else:
							x1 = int(t[1][index])
							x3 = int(t[1+column][index])
							virtual_bias = ""
							bias = x1
							if not hdot:
								bias += (x3 - x1) * (i - 1)
							else:
								bias += -(row - i) * (x3 - x1) - (x3 - x1)
								if x3 != x1:
									if x3 == x2 + 1:
										virtual_bias += ("+" if virtual_bias else "") + virtual_column
									elif x1 == x2 + 1:
										virtual_bias += "-" + virtual_column
									else:
										virtual_bias += ("+" if virtual_bias and x2 > x1 else "") + str(x2 - x1) + virtual_column
							if bias == 0:
								value += virtual_bias
							else:
								value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
					return value
					flag = True
			elif j > 2:
				value = ""
				if re.sub("\d", "*", t[1]) == re.sub("\d", "*", t[2]):
					for index in range(len(t[1])):
						if not t[1][index].isnumeric():
							value += t[1][index]
						else:
							x1 = int(t[1][index])
							x2 = int(t[2][index])
							virtual_bias = ""
							bias = x1
							if not vdot:
								bias += (x2 - x1) * (j - 1)
							else:
								bias += -(column - j) * (x2 - x1) - (x2 - x1)
								if x2 != x1:
									if x2 == x1 + 1:
										virtual_bias += virtual_column
									elif x1 == x2 + 1:
										virtual_bias += "-" + virtual_column
									else:
										virtual_bias += str(x2 - x1) + virtual_column
							if bias == 0:
								value += virtual_bias
							else:
								value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
					return value
					flag = True
			if not flag and re.match(".*[a-zA-Z]_\{11\}", t[1]):
				if not vdot and not hdot:
					return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", t[1])
				elif vdot and hdot:
					return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", t[1])
				elif vdot:
					return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", t[1])
				else:
					return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + str(j) + "}", t[1])
			if not flag:
				return ""
	else:
		return ""
