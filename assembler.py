def assemble(i):
    result=''
    l1=[]
    l2=[]
    l1=i.split( )
    l2=l1[-1].split(',')
    l1.pop()
    l=l1+l2
    if len(l)==2:
        l.append('NULL')

    if l[0]=='MOV':
        if l[1]=='A':
            if l[2]=='B':
                result='00100000'
                return result
            else:
                result='0000'+l[2]
                return result

        elif l[1]=='B':
            if l[2]=='A':
                result='00110000'
                return result
            else:
                result='0001'+l[2]
                return result

    if l[0]=='ADD':
        if l[1]=='A':
            return '0100'+l[2]
        elif l[1]=='B':
            return '0101'+l[2]
        else: 
            return 'error!'

    if l[0]=='IN':
        if l[2]!='NULL':
            return 'error!'
        if l[1]=='A':
            return '01100000'
        elif l[1]=='B':
            return '01110000'
        else:
            return 'error!'

    if l[0]=='OUT':
        if l[2]!='NULL':
            return 'error!'
        if l[1]=='B':
            return '10010000'
        else:
            return '1000'+l[1]

    if l[0]=='JMP':
        if l[2]!='NULL':
            return 'error!'
        else:
            return '1010'+l[1]

    if l[0]=='JNC':
        if l[2]!='NULL':
            return 'error!'
        else:
            return '1011'+l[1]

    else:
        return 'Wrong instruction'

# test
i='MOV A,1101'
print(assemble(i))
i='MOV B,1101'
print(assemble(i))
i='MOV A,B'
print(assemble(i))
i='MOV B,A'
print(assemble(i))
i='ADD A,1101'
print(assemble(i))
i='ADD B,1101'
print(assemble(i))
i='IN A'
print(assemble(i))
i='IN B'
print(assemble(i))
i='OUT 1101'
print(assemble(i))
i='OUT B'
print(assemble(i))
i='JMP 1101'
print(assemble(i))
i='JNC 1101'
print(assemble(i))