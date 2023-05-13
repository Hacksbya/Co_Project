#initialising the flags for different error cases
error_a,error_b,error_c,error_d,error_e,error_f,error_g,error_h,error_i=0,0,0,0,0,0,0,0,0
error_count=0

#functions for printing the different types of machine codes sepereated by their types
def Fn_A(i):
    s=(Type_A[i[0]])
    s+='00'
    s+=register[i[1]]
    s+=register[i[2]]
    s+=register[i[3]]
    print(s)


def Fn_B(i):
    s=(Type_B[i[0]])
    s+=register[i[1]]
    p=i[2]
    p=p[1:]
    s+=format(int(p),'07b')
    print(s)

def Fn_C(i):
    s=(Type_C[i[0]])
    s+='00000'
    s+=register[i[1]]
    s+=register[i[2]]
    print(s)


def Fn_D(i):
    s=(Type_D[i[0]])
    s+='0'
    s+=register[i[1]]
    s+=variable['var'][i[2]]
    print(s)


def Fn_E(i):
    s=(Type_E[i[0]])
    s+='0000'
    s+=new_label[i[1]]
    print(s)


def Fn_F(i):
    s=(Type_F[i[0]])
    s+='00000000000'
    print(s)


#main program
f=open("E:\Projects\CO_CourseProject\co.txt.txt")
assemb_prg=[]
for i in f.readlines():
    words=i.strip().split()
    assemb_prg.append(words)

#checking for the error of type_I
if assemb_prg[-1][-1]!="hlt":
    error_i=1
    error_count+=1

#removing the empty elements of the program given
for i in assemb_prg:
    if i==[]:
        assemb_prg.remove(i)

variable={}
var=[]


#assemb_prg is a 2-D list containing all the words of the progaram seperated as seperate words
for inst in assemb_prg:
    if inst[0]=='var':
        if "var" in variable:
            variable["var"].append(inst[1])
        else:
            variable["var"]=[inst[1]]
#var is a 2-D list having variables inside the second list
for j in variable.values():
    var.append(j)

variable_dict = {var: i for i, var in enumerate(variable['var'])}
variable['var'] = variable_dict

#coverting all the variables in the list to None
for i,j in variable.items():
    for var in range(len(j)):
        assemb_prg[var]=None

#removing all the none in the program
i=0
while(i<len(assemb_prg)):
    if None in assemb_prg:
        assemb_prg.remove(None)
    i+=1

#assigning the addrersses to the variables
for k in variable.values():
    for i,j in k.items():
        k[i]=format(len(assemb_prg)+j,'07b')

label={}
c=0

#removing the halt_label: form the assemb_prg 
#+ checking for the error of type_H
error_h=1
for i in assemb_prg:
    if ':' in i[0]:
        error_h=0
        error_count+=1
        label[i[0]]=format(assemb_prg.index(i),'07b')
        i.remove(i[0])

#assigning the address to the hlt statement
new_label = {}
for k, v in label.items():
    new_label[k.rstrip(':')] = v


#print(variable,"\n",assemb_prg)

Type_A={"add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100"}
Type_B={"mov":"00010","rs":"01000","ls":"01001"}
Type_C={"mov":"00011","div":"00111","not":"01101","cmp":"01110"}
Type_D={"ld":"00100","st":"00101"}
Type_E={"jmp":"01111","jlt":"11100","jgt":"11101","je":"11111"}
Type_F={"hlt":"11010"}

register={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

#checking for the error of type E
for i in assemb_prg:
    if i[0] in Type_B:
        temp_e=i[2][1:]
        if int(temp_e)>=128:
            error_e=1
            error_count+=1

#handeling errors because of different flags that could be raised because of possible errors
if(error_count==1):
    if(error_a==1):
        print("Typo in instruction name or register name")
    if(error_b==1):
        print("Use of undefined variables")
    if(error_c==1):
        print("Use of undefined labels")
    if(error_d==1):
        print("Illegal use of FLAGS register")
    if(error_e==1):
        print("Illegal Immediate values (more than 7 bits)")
    if(error_f==1):
        print("Misuse of labels as variables or vice-versa")
    if(error_g==1):
        print("Variables not declared at the beginning")
    if(error_h==1):
        print("Missing hlt instruction")
    if(error_i==1):
        print("hlt not being used as the last instruction")
        
elif(error_count>1):
    print("General Syntax Error")



#printing the machine code by calling different functions
for i in assemb_prg:
    if i[0] in Type_A.keys():
        Fn_A(i)
    elif i[0] in Type_B:
        Fn_B(i)
    elif i[0] in Type_C:
        Fn_C(i)
    elif i[0] in Type_D:
        Fn_D(i)
    elif i[0] in Type_E:
        Fn_E(i)
    elif i[0] in Type_F:
        Fn_F(i)

