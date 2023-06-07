import sys


def Fn_A(x):
    s = x[0:5] # opcode
    r1 = x[7:10] # reg 1
    r2 = x[10:13] # reg 2
    r3 = x[13:16] # reg 3
    a = register[r2] # value of reg 2
    b = register[r3] # value of reg 3
    if s == "00000": # ADD operation
        c = int(a,2)+int(b,2)
        if c>127: # overflow
            register["111"] = "000000000000"+"1"+flag[14:]
            register[r1] = format(0,'016b')
        else:
            c = format(c,'016b')
            register[r1] = c
    elif s == "00001": # SUB operation 
        c = int(a,2) - int(b,2)
        if c<0: # overflow 
            register["111"] = "000000000000"+"1"+flag[14:]
            register[r1] = format(0,'016b')
        else:
            c = format(c,'016b')
            register[r1] = c
    elif s == "00110": # MUL operation
        c = int(a,2) * int(b,2)
        if c>127: # overflow
            register["111"] = "000000000000"+"1"+flag[14:]
            register[r1] = format(0,'016b')
        else:
            c = format(c,'016b')
            register[r1] = c
    elif s == "01010": # XOR operation
        c = int(a,2) ^ int(b,2)
        c = format(c,'016b')
        register[r1] = c
    elif s =="01011": # OR operation
        c = int(a,2) or int(b,2)
        c = format(c,'016b')
        register[r1] = c
    elif s =="01100":# AND operation
        c = int(a,2) and int(b,2)
        c = format(c,'016b')
        register[r1] = c
    for i in register.values(): # sys.stdout.writeing
            sys.stdout.write(i)
        

def Fn_B(x):
    s = x[0:5] # opcode
    r1 = x[6:9] # reg 1
    r2 = x[9:] # immediate value
    a = (register[r1])
    b = int(register[r2],2)
    if s == "00010": # mov type b
        register[r1] = format(b,'016b')
    elif s == "01000": # right shift
        register[r1] = a >> b
    elif s == "01001": # left shift
        register[r1] =  a << b
    for i in register.values(): # sys.stdout.writeing
            sys.stdout.write(i)


def Fn_C(x):
    s = x[0:5] # opcode
    r1 = x[10:13] # reg 1
    r2 = x[13:16] # reg 2
    a = int(register[r1],2) # value of reg 1
    b = int(register[r2],2) # value of reg 2
    if s == "00011": # mov type c
        register[r1] = format(b,'016b')
    elif s == "00111": # divide operation 
        if b == 0:
            register["111"] = "000000000000"+"1"+flag[14:]
            register["000"] = format(0,'016b')
            register["001"] = format(0,'016b')
        else:
            register["000"] = format((a//b),'016b')
            register["001"] = format((a%b),'016b')
    elif s == "01101":# not operation
        register[r1] = not b
    elif s == "01110": # cmp operation and changing value of FLAGS register
        if a>b: # greater than flag
            register["111"] = flag[0:14]+"1"+flag[15:]
        elif a<b: # less than flag
            register["111"] = flag[0:13]+"1"+flag[14:]
        else: # equal flag
            register["111"] = flag[0:15]+"1"
    for i in register.values(): # sys.stdout.writeing
            sys.stdout.write(i)


def Fn_D(x):
    pass

def Fn_E(x):
    pass

Type_A=["00000","00001","00110","01010","01011","01100"]
Type_B=["00010","01000","01001"]
Type_C=["00011","00111","01101","01110"]
Type_D=["00100","00101"]
Type_E=["01111","11100","11101","11111"]
Type_F=["11010"]

register={"000":"0000000000000100","001":"0000000000000000","010":"0000000000000000","011":"0000000000000000","100":"0000000000000000","101":"0000000000000010","110":"0000000000000000","111":"0000000000000000"}

flag = register["111"]
#main program
# f=open("stdin.txt")
assemb_prg=[]
# for i in f.readlines():
#     words=i.strip().split()
#     assemb_prg.append(words)
for kx in sys.stdin:
    words=kx.strip().split()
    assemb_prg.append(words)   



#removing the empty elements of the program given
for i in assemb_prg:
    if i==[]:
        assemb_prg.remove(i)


for i in range(len(assemb_prg)):
    sys.stdout.write((format(i,'07b')))
    sys.stdout.write("        ")
    pl = assemb_prg[i][0]
    ele = assemb_prg[i][0][0:5]
    if ele in Type_A:
        Fn_A(pl)
    elif ele in Type_B:
        Fn_B(pl)
    elif ele in Type_C:
        Fn_C(pl)
    elif ele in Type_D:
        Fn_D(pl)
    elif ele in Type_E:
        Fn_E(pl)
    else:
        for i in register.values(): # sys.stdout.writeing
            sys.stdout.write(i)
