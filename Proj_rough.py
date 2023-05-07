f=open("co.txt")
assemb_prg=[]
for i in f.readlines():
    words=i.strip().split()
    assemb_prg.append(words)
for i in assemb_prg:
    if i==[]:
        assemb_prg.remove(i)
variable={}


for inst in assemb_prg:
    if inst[0]=='var':
        if "var" in variable:
            variable["var"].append(inst[1])
        else:
            variable["var"]=[inst[1]]

for i,j in variable.items():
    for var in range(len(j)):
        assemb_prg[var]=None
i=0
while(i<len(assemb_prg)):
    if None in assemb_prg:
        assemb_prg.remove(None)
    i+=1

print(variable,"\n",assemb_prg)

