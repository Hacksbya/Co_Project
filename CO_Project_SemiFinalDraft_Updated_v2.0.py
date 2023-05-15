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
    s+='0'
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
f=open("co.txt")
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

#checking for error of type G
if len(var)!=0:
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
else:
    for i in assemb_prg:
        if len(i)==3:
            if 'var' in i[2]:
                error_g=1
            else:
                break
    error_count+=1


label={}
c=0

#removing the halt_label: form the assemb_prg 
#+ checking for the error of type_H
error_h=1
for i in assemb_prg:
    if ':' in i[0]:
        error_h=0
        label[i[0]]=format(assemb_prg.index(i),'07b')
        i.remove(i[0])

if(error_h==1):
    error_count+=1

#assigning the address to the hlt statement
new_label = {}
for k, v in label.items():
    new_label[k.rstrip(':')] = v

#removing label
for i in assemb_prg:
    if i==[]:
        assemb_prg.remove(i)

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

#checking for error of type A
def detect_typo(assemb_prg):          
    inst_name = ["add" , "sub" , "mul" , "xor" , "or" , "and" , "mov" , "div" , "not" , "cmp" , "ld" , "st" , "jmp" , "jlt" , "jgt" , "je" , "hlt"]
    reg_name = ["R0" , "R1" ,"R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]
    isError = False
    for i in assemb_prg:           #i -> instruction
        if i[0] not in inst_name:
            isError = True
        
        for r in i[1:]:  
                if 'var' not in r:
                    if 'label' not in r:
                            if '$' not in r:
                                if "R" in r:
                                    if r not in reg_name:
                                        isError = True   
               
    return isError 

if detect_typo(assemb_prg) == True:
    error_a = 1
    error_count += 1

#checking for error of type B
def detect_undefined_var(assemb_prg):
    var_set = set()
    isError = False
    for i in assemb_prg:
        var_set.update(i[1:])
    for j in var_set:
        if j not in register and j not in variable['var']:
            isError = True                       #print the error message           
    return isError  

if detect_undefined_var(assemb_prg) == True:
    error_b = 1
    error_count += 1

#checking for error of type C
def detect_undefined_label(assemb_prg):             
    labels = set(new_label.keys())
    isError = False
    for i in assemb_prg:
        if i[0] in ["jmp", "jlt", "jgt", "je"]:
            if i[1] not in labels:
                isError = True
            elif 'label' in label:
                isError = True
    return isError
                
if detect_undefined_label(assemb_prg) == True:
    error_c = 1
    error_count += 1 


#checking for error of type D``
def detect_illegal_flags(assemb_prg):          
    isIllegal = False

    for i in assemb_prg:
        if i[0] in ["add", "sub", "mul", "xor", "or", "and", "div", "not", "cmp"]:
            for j in i[1:]:
                if j == "FLAGS":
                    isIllegal = True
    
    return isIllegal

if detect_illegal_flags(assemb_prg) == True:
    error_d = 1
    error_count += 1

#checking of error of type_F

def Error_f(assemb_prg):
    isError=False
    for i in assemb_prg:
        if i[0] in ["jmp", "jlt", "jgt", "je"]:
            if 'label' not in i[1]:
                isError=True

        if i[0] in ["add" , "sub" , "mul" , "xor" , "or" , "and" , "mov" , "div" , "not" , "cmp" , "ld" , "st" ]:
            if 'label' in i[1:0]:
                isError=True
    
    return isError


if Error_f(assemb_prg) == True:
    error_f=1
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
    exit()        
elif(error_count>1):
    print("General Syntax Error")
    exit()


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

