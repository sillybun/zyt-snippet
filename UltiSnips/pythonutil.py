import re

def generate_matrix_element(i, j, row, column, virtual_row, virtual_column, ht, vt):
    vdot = False
    hdot = False
    leftp = "{"
    rightp = "}"
    # print(i, j, row, column, virtual_row, virtual_column)
    # print(ht)
    # print(vt)
    if i > 1 and ht[j].strip() == "\\cdots":
        vdot = True
    if j > 1 and vt[i].strip() == "\\vdots":
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
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            x3 = int(vt[2][index])
                            value += str((x2 - x1) * (j-1) + (x3 - x1) * (i-1) + x1)
                    return value
                elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                else:
                    return ""
            elif i > 2:
                value = ""
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                        else:
                            x1 = int(ht[1][index])
                            x3 = int(vt[2][index])
                            value += str((x3 - x1) * (i - 1) + x1)
                    return value
                elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                else:
                    return ""
            elif j > 2:
                value = ""
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            value += str((x2 - x1) * (j-1) + x1)
                    return value
                elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                else:
                    return ""
            elif re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
            else:
                return ht[1]
        else:
            vdot = False
            hdot = False
            if any([x.strip() == "\\vdots" for x in vt[:-1]]):
                hdot = True
            if any([x.strip() == "\\cdots" for x in ht[:-1]]):
                vdot = True
            flag = False
            biasandvirtualbias = False
            if i > 1 and j > 1:
                value = ""
                underline = False
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            value += ht[1][index]
                            biasandvirtualbias = False
                            if ht[1][index] == "_":
                                underline = True
                            else:
                                underline = False
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            x3 = int(vt[2][index])
                            virtual_bias = ""
                            bias = x1
                            if underline and ht[1][index-1] == "_":
                                value += leftp
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
                                    if x3 == x1 + 1:
                                        virtual_bias += ("+" if virtual_bias else "") + virtual_row
                                    elif x1 == x3 + 1:
                                        virtual_bias += "-" + virtual_row
                                    else:
                                        virtual_bias += ("+" if virtual_bias and x3 > x1 else "") + str(x3 - x1) + virtual_row
                            if index > 0 and ht[1][index-1].isnumeric() and (biasandvirtualbias or (bias and virtual_bias)):
                                value += ","
                            biasandvirtualbias = bias and virtual_bias
                            if bias == 0:
                                value += virtual_bias
                            else:
                                value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
                            if underline and (index == len(ht[1])-1 or not ht[1][index+1].isnumeric()):
                                value += rightp
                    return value
                    flag = True
            elif i > 2:
                value = ""
                underline = False
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", vt[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            biasandvirtualbias = False
                            value += ht[1][index]
                            if ht[1][index] == "_":
                                underline = True
                            else:
                                underline = False
                        else:
                            x1 = int(ht[1][index])
                            x3 = int(vt[2][index])
                            virtual_bias = ""
                            bias = x1
                            if underline and ht[1][index-1] == "_":
                                value += leftp
                            if not hdot:
                                bias += (x3 - x1) * (i - 1)
                            else:
                                bias += -(row - i) * (x3 - x1) - (x3 - x1)
                                if x3 != x1:
                                    if x3 == x1 + 1:
                                        virtual_bias += ("+" if virtual_bias else "") + virtual_row
                                    elif x1 == x3 + 1:
                                        virtual_bias += "-" + virtual_row
                                    else:
                                        virtual_bias += ("+" if virtual_bias and x3 > x1 else "") + str(x3 - x1) + virtual_row
                            if index > 0 and ht[1][index-1].isnumeric() and (biasandvirtualbias or (bias and virtual_bias)):
                                value += ","
                            biasandvirtualbias = bias and virtual_bias
                            if bias == 0:
                                value += virtual_bias
                            else:
                                value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
                            if underline and (index == len(ht[1])-1 or not ht[1][index+1].isnumeric()):
                                value += rightp
                    return value
                    flag = True
            elif j > 2:
                value = ""
                underline = False
                if re.sub("\d", "*", ht[1]) == re.sub("\d", "*", ht[2]):
                    for index in range(len(ht[1])):
                        if not ht[1][index].isnumeric():
                            biasandvirtualbias = False
                            value += ht[1][index]
                            if ht[1][index] == "_":
                                underline = True
                            else:
                                underline = False
                        else:
                            x1 = int(ht[1][index])
                            x2 = int(ht[2][index])
                            virtual_bias = ""
                            bias = x1
                            if underline and ht[1][index-1] == "_":
                                value += leftp
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
                            if index > 0 and ht[1][index-1].isnumeric() and (biasandvirtualbias or (bias and virtual_bias)):
                                value += ","
                            biasandvirtualbias = bias and virtual_bias
                            if bias == 0:
                                value += virtual_bias
                            else:
                                value += virtual_bias + ("+" if virtual_bias and bias > 0 else "") + str(bias)
                            if underline and (index == len(ht[1])-1 or not ht[1][index+1].isnumeric()):
                                value += rightp
                    return value
                    flag = True
            if not flag and re.match(".*[a-zA-Z]_\{11\}", ht[1]):
                if not vdot and not hdot:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + str(j) + "}", ht[1])
                elif vdot and hdot:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", ht[1])
                elif vdot:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + str(i) + "," + virtual_column + ("-" + str(column - j) if j != column else "") + "}", ht[1])
                else:
                    return re.sub("([a-zA-Z])_\{11\}", "\\g<1>_{" + virtual_row + ("-" + str(row - i) if i != row else "") + "," + str(j) + "}", ht[1])
                flag = True
            elif not flag and (i == 1 or j == 1):
                return ht[1]
                flag = True
            if not flag:
                return ""
    else:
        return ""

def first_p1_not_p2(line, p1, p2):
    p1s = re.search(p1, line)
    p2s = re.search(p2, line)
    if p1s and not p2s:
        return 1
    if p2s and not p1s:
        return -1
    if not p1s and not p2s:
        return 0
    if [x for x in re.finditer(p1, line)][0].span()[0] < [x for x in re.finditer(p2, line)][0].span()[0]:
        return 1
    else:
        return -1

def last_p1_not_p2(line, p1, p2):
    p1s = re.search(p1, line)
    p2s = re.search(p2, line)
    if p1s and not p2s:
        return 1
    if p2s and not p1s:
        return -1
    if not p1s and not p2s:
        return 0
    if [x for x in re.finditer(p1, line)][-1].span()[0] > [x for x in re.finditer(p2, line)][-1].span()[0]:
        return 1
    else:
        return -1
