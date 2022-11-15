import copy
import itertools as it

# parser
# Read file
in_file = open('input4')
in_data = in_file.readlines()

# Delete '\n'
l = len(in_data)
i = 0
while i < l:
    in_data[i] = in_data[i].rstrip()
    i += 1

# print(in_data)
cubeList = []
resList = []
# Generate lists for cubes for following operations
for a in in_data:
    al = a.split(' ')
    cubeList.append(list(al[0]))
    resList.append(list(al[1]))

# print(cubeList)
# print(resList)

on_set = []
dc_set = []
Mcurrf = ['-']*len(cubeList[0])
i = 0
while i < len(resList):
    if resList[i] == ['1']:
        on_set.append(cubeList[i])
    if resList[i] == ['x']:
        dc_set.append(cubeList[i])
    i += 1


def factorize(cubeList, factor):
    # Cube format: [['-', '0', '-', '1'], ['1', '-', '1', '0']]

    # decide factor
    ini = 0
    oui = 0
    f1 = 0
    f2 = 0
    r = 0
    while ini < len(cubeList[0]):
        while oui < len(cubeList):
            if cubeList[oui][ini] != '-':
                f1 += 1
            oui += 1
        if f1 > f2:
            f2 = f1
            r = ini
        ini += 1
        f1 = 0
        oui = 0

    # factor format: ['-', '0', '1', '-']
    cofactor_set0 = []
    fac0 = copy.deepcopy(factor)
    fac0[r] = '0'
    cofactor_set1 = []
    fac1 = copy.deepcopy(factor)
    fac1[r] = '1'

    for a in cubeList:
        if a[r] == '-':
            cofactor_set0.append(a)
            cofactor_set1.append(a)

        elif a[r] == '0':
            i = copy.deepcopy(a)
            i[r] = '-'
            cofactor_set0.append(i)

        elif a[r] == '1':
            i = copy.deepcopy(a)
            i[r] = '-'
            cofactor_set1.append(i)

    return fac0, cofactor_set0, fac1, cofactor_set1


# Shannon Expansion
cofac0 = []
cofac1 = []
fac0 = []
fac1 = []

offcover = []

currf = ['-']*len(on_set[0])
fa_list = [[cubeList, currf]]
# print('fa_list=', fa_list)
# Obtain the offcover
new_fa_list = []
i = 0
while fa_list:
    while i < len(fa_list):
        fac0, cofac0, fac1, cofac1 = factorize(fa_list[i][0], fa_list[i][1])

        if Mcurrf in cofac0:  # On set check, if 1, ignore
            pass
        elif cofac0:  # Not finished, keep factorizing
            new_fa_list.append([cofac0, fac0])
        elif cofac0 == []:  # Off set check, target cover
            offcover.append(fac0)

        if Mcurrf in cofac1:
            pass
        elif cofac1:
            new_fa_list.append([cofac1, fac1])
        elif cofac1 == []:
            offcover.append(fac1)

        i += 1
    i = 0
    fa_list = copy.deepcopy(new_fa_list)
    new_fa_list = []

# print('off-cover=', offcover)

# Negate&Expand


def neg_and_expand(offcover):
    expand_list = []
    i = 0
    for a in offcover:
        ml = []
        while i < len(offcover[0]):
            mt = copy.deepcopy(Mcurrf)
            if a[i] == '-':
                pass

            elif a[i] == '1':
                mt[i] = '0'
                ml.append(mt)

            elif a[i] == '0':
                mt[i] = '1'
                ml.append(mt)
            i += 1
        i = 0
        expand_list.append(ml)
    return expand_list


# print(neg_and_expand(offcover))
# function: and, simplify


def m_and(l1, l2):
    i = 0
    res = []
    while i < len(l1):
        if (l1[i] == '0' and l2[i] == '1') or (l1[i] == '1' and l2[i] == '0'):  # No this term
            return 0, res
        elif l1[i] == '-' and l2[i] == '-':
            res.append('-')
        elif l1[i] == l2[i]:
            res.append(l1[i])
        elif (l1[i] == '1' and l2[i] == '-') or (l1[i] == '-' and l2[i] == '1'):
            res.append('1')
        elif (l1[i] == '0' and l2[i] == '-') or (l1[i] == '-' and l2[i] == '0'):
            res.append('0')
        i += 1
    return 1, res


def contain(l1, l2):  # check whether 1 contain 2
    i = 0
    while i < len(l1):
        if (l1[i] != '-' and l2[i] == '-') or (l1[i] == '0' and l2[i] == '1') or (l1[i] == '1' and l2[i] == '0'):
            return 0
        i += 1
    return 1


def simplify(l):
    i1 = 0
    i2 = 1
    while i1 < len(l):
        while i2 < len(l):
            if contain(l[i1], l[i2]) or l[i1] == l[i2]:
                l.pop(i2)
            else:
                i2 += 1
        i1 += 1
        i2 = i1+1

    l.reverse()
    i1 = 0
    i2 = 1
    while i1 < len(l):
        while i2 < len(l):
            if contain(l[i1], l[i2]) or l[i1] == l[i2]:
                l.pop(i2)
            else:
                i2 += 1
        i1 += 1
        i2 = i1+1
    return l


def merge_till_last(offcover):
    l = neg_and_expand(offcover)
    while len(l) > 1:
        product = []
        for a in l[0]:
            for b in l[1]:
                t = []
                check, t = m_and(a, b)
                if (check):
                    product.append(t)

        product_s = simplify(product)
        l.pop(0)
        l.pop(0)
        l.append(product_s)
    return l[0]


merge_result = merge_till_last(offcover)

# Eliminate DC
i = 0
while i < len(merge_result):
    if merge_result[i] in dc_set:
        merge_result.pop(i)
    i += 1


def m_check(c):  # check whether a cube contain '-'
    i = 0
    while i < len(c):
        if c[i] == '-':
            return 1
        i += 1
    return 0


def expand(c):  # expand a cube
    i = 0
    r = []
    while i < len(c):
        if c[i] == '-':
            c0 = copy.deepcopy(c)
            c0[i] = '0'
            r.append(c0)
            c1 = copy.deepcopy(c)
            c1[i] = '1'
            r.append(c1)
            return r
        i += 1
    return c


def expand_all(cl):
    cli = copy.deepcopy(cl)
    i = 0
    rt = []
    while i < len(cli):
        if m_check(cli[i]):
            rt = expand(cli[i])
            cli.pop(i)
            cli = cli+rt
        else:
            i += 1
    return cli


exp_result = expand_all(merge_result)
exp_result = simplify(exp_result)
# print('=============')
# print(exp_result)
# print('merge')
# print(merge_result)

# Essential Check
Er = []
i = 0
for a in exp_result:
    for b in merge_result:
        if contain(b, a):
            i += 1
            mem = copy.deepcopy(b)
            if i > 1:
                i = 0
                break
    if i == 1:
        Er.append(mem)
        i = 0
Er.sort()
i = 0
j = 1
while i < len(Er):
    m = copy.deepcopy(Er[i])
    while j < len(Er):
        if m == Er[j]:
            Er.pop(j)
        else:
            j += 1
    i += 1
    j = i+1

print('Er=', Er)

R = copy.deepcopy(merge_result)
i = 0
for a in Er:
    while i < len(R):
        if R[i] == a:
            R.pop(i)
        else:
            i += 1
    i = 0

# Totally rundant check
# Obtain Rp By removing Rt

i = 0
fullEr = []
fullEr = expand_all(Er)

i = 0
while i < (len(R)):
    R_expand = []
    R_expand = expand_all([R[i]])
    checkbit = 1
    for a in R_expand:
        checkbit = checkbit and (a in fullEr)

    if checkbit:
        R.pop(i)
    else:
        i += 1

print('Rp=', R)

# Obtain left cube which needed to be cover
Mp = copy.deepcopy(exp_result)
i = 0
for a in Er:
    while i < len(Mp):
        if contain(a, Mp[i]):
            Mp.pop(i)
        else:
            i += 1
    i = 0

print('Mp=', Mp)


def get_Result(Rp, Mp):
    if (len(Rp) == 0 and len(Mp) == 0):
        print('Since no Rp left, result is Er')
        return None
    i = 0
    while i < len(Rp[0]):
        for a in it.combinations(Rp, i):
            t = copy.deepcopy(Mp)
            j = 0
            for b in a:
                while j < len(t):
                    if contain(b, t[j]):
                        t.pop(j)
                    else:
                        j += 1
                j = 0
            if len(t) == 0:
                return a
        i += 1


M = get_Result(R, Mp)
if (M):
    final = []
    for a in Er:
        final.append(a)
    for a in M:
        final.append(a)
    print('Result is:')
    for a in final:
        res = ''
        for b in a:
            res = res+b
        print(res)
else:
    final = []
    for a in Er:
        final.append(a)
    print('Result is:')
    for a in final:
        res = ''
        for b in a:
            res = res+b
        print(res)
