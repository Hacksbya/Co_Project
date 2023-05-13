f=open("co.txt")
assemb_prg=[]
for i in f.readlines():
    words=i.strip().split()
    assemb_prg.append(words)
for i in assemb_prg:
    if i==[]:
        assemb_prg.remove(i)
variable={}
var=[]

for inst in assemb_prg:
    if inst[0]=='var':
        if "var" in variable:
            variable["var"].append(inst[1])
        else:
            variable["var"]=[inst[1]]

for j in variable.values():
    var.append(j)

variable_dict = {var: i+1 for i, var in enumerate(variable['var'])}
variable['var'] = variable_dict


for i,j in variable.items():
    for var in range(len(j)):
        assemb_prg[var]=None
i=0
while(i<len(assemb_prg)):
    if None in assemb_prg:
        assemb_prg.remove(None)
    i+=1

for k in variable.values():
    for i,j in k.items():
        k[i]=format(len(assemb_prg)+j,'07b')
label={}
c=0
for i in assemb_prg:
    if 'label' in i[0]:
        label[i[0]]=format(assemb_prg.index(i),'07b')
        i.remove(i[0])

new_label = {}
for k, v in label.items():
    new_label[k.rstrip(':')] = v
print(new_label)

print(variable,"\n",assemb_prg)

type_opc={"TA":{"add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100"},
          "TB":{"mov":"00010","rs":"01000","ls":"01001"},
          "TC":{"mov":"00011","div":"00111","not":"01101","cmp":"01110"},
          "TD":{"ld":"00100","st":"00101"},
          "TE":{"jmp":"01111","jlt":"11100","jgt":"11101","je":"11111"},
          "TF":{"hlt":"11010"}}

register={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":110,"FLAGS":"111"}


for i in assemb_prg:
    if i[0]=='mov':
        if '$' in i[2]:
            for j,k in type_opc.items():
                if j=='TB':
                    if i[0] in k:
                        print(format(assemb_prg.index(i),'07b'),'-',k[i[0]])
        else:
            # mov["TC"].append(i)
            for j,k in type_opc.items():
                if j=='TC':
                    if i[0] in k:
                        print(format(assemb_prg.index(i),'07b'),'-',k[i[0]])

    else:
        for j,k in type_opc.items():
            if i[0] in k:
                        print(format(assemb_prg.index(i),'07b'),'-',k[i[0]])



