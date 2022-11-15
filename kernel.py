import copy
# Input
# inM=[
#     [0,1,1,1,1],
#     [1,0,1,1,1],
#     [1,1,0,1,1]
# ]
# lit_name=['a','b','c','d','e']

inM = [
    [0, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0],
    [1, 0, 1, 1, 0, 0]
]
lit_name = ['a', '~b', 'b', 'c', 'd', 'e']

kernelMatrixList = []
# Make it cube free


def cube_free_check(m):
    # Check whether dividable
    # Input: Matrix m
    # Output:
    # If cube free, None;
    # Else: Cube
    indexList = []
    i = 0
    while i < len(m[0]):
        checkbit = 1
        ignore_check = []
        for a in m:
            if a[i] < 0:
                ignore_check.append(-1)
                continue
            checkbit = checkbit and a[i]

        if checkbit and len(ignore_check) != len(m):
            indexList.append(i)
        i += 1
    if indexList:
        return indexList
    else:
        return None


def dividable_check(m):
    i = 0
    indexList = []
    while i < len(m[0]):
        c = 0
        for a in m:
            if a[i] == 1:
                c += 1
        if c >= 2:
            indexList.append(i)
        i += 1
    if indexList:
        return indexList
    else:
        return None


def divide(m, index):
    # m: matrix
    # index: colomn to be divided
    new_m = copy.deepcopy(m)
    row2rm = []  # Row to remove

    # Obtain the row with 0
    row0 = []
    i = 0
    while i < len(m):
        if m[i][index] == 0:
            row0.append(i)
        i += 1

    # Remove the row with 0
    for a in row0:
        i = 0
        while i < len(m[0]):
            new_m[a][i] = -1
            i += 1

    # Remove the colomn
    i = 0
    while i < len(new_m):
        new_m[i][index] = -1
        i += 1

    return new_m


def kernelPrint(m):
    out = ''
    for a in m:
        curr = ''
        i = 0
        while i < len(a):
            if a[i] == 1:
                curr = curr+str(lit_name[i])
            i += 1
        if curr != '' and out != '':
            out = out+'+'+curr
        if curr != '' and out == '':
            out = out + curr
    return out


class operation_node:
    def __init__(self, matrix, finished, finishedList=[]):
        self.matrix = matrix
        if finishedList:
            finishedList.append(finished)
            self.finished = finishedList
        else:
            self.finished = [finished]


# Start
# Make it cube free
# public literals
pub = cube_free_check(inM)
pubname = []
finishList = []
currM = copy.deepcopy(inM)

if pub:
    pub.sort(reverse=True)
    for a in pub:
        pubname.append(a)
        currM = divide(currM, a)
        finishList.append(operation_node(currM, None))
i = 0
nodeList = []
matrixList = []
divideList = dividable_check(currM)

for a in divideList:
    node = operation_node(divide(currM, a), a)
    nodeList.append(node)

for a in nodeList:
    finishList.append(a)
if dividable_check(inM):
    finishList.append(operation_node(inM, None))

while nodeList:
    i = 0
    indexList = dividable_check(nodeList[0].matrix)
    if indexList:
        while i < len(indexList):
            if indexList[i] < max(nodeList[0].finished):
                indexList.pop(i)
            else:
                i += 1

        for a in indexList:
            newNodeM = divide(nodeList[0].matrix, a)
            newFinish = copy.deepcopy(nodeList[0].finished)
            newnode = operation_node(newNodeM, a, newFinish)
            nodeList.append(newnode)
            finishList.append(newnode)

    nodeList.pop(0)

K_List = []
co_K0_List = []

for a in finishList:
    if not cube_free_check(a.matrix):
        K_List.append(a.matrix)
    if not dividable_check(a.matrix):
        co_K0_List.append([a.finished, a.matrix])

# Print input
print('Input: f='+kernelPrint(inM)+'\n')

# Print results
print('Kernels:')
for a in K_List:
    print('================================================')
    print(kernelPrint(a))
    print('')
    print('In matrix form:')
    for b in a:
        print(b)

print('================================================')
print('0-level kernel set and paired cokernel set:')
print('')
for a in co_K0_List:
    # print('K0:',a[1])
    print('K0:', kernelPrint(a[1]))
    i = 0
    CK0 = ''
    if pub:
        a[0] = a[0]+pub

    for b in a[0]:
        CK0 = CK0+lit_name[b]
        i += 1
    print('CK0:', CK0)
    print('')
