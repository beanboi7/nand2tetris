
from symboltable import *
import re

symb = SymbolTable()

f = open("../add/Add.asm","r")
line_count = 0
varSpace = 16
labels = {}
temp_key = ''
AReg = ''
C_msb = '111'
A = ""
jmp = ''
dest = ''
comp = ''
inst = ''

for line in f:
    if line.startswith("//") or line.startswith("\n") or line == '':
        continue
    if temp_key in labels:
        pass
    elif temp_key not in labels:
        labels[temp_key] = line_count
    
    line = line.replace("\n", "")
    line = line.strip()
    
    if line.startswith("("):
        line = line.lstrip("(") 
        line = line.rstrip(")")
        temp_key = line
        continue
    
    
    line_count +=1 
#end of 1st pass 

# print(labels)

f.seek(0)
for line in f:
    line = line.lstrip()
    line = line.strip()
    line = line.replace("\n","")

    if line.startswith("("):
        continue
    if line.startswith("//") or line.startswith("\n") or line == '':
        continue
    
    elif "//" in line:
        line = line.split("//", 1)[0]
        line = line.strip()

    
    if line.startswith("@"):
        try:
            if line[1] == "R" or line[1] == "r" and type(int(line[2])) == int:
                AReg = symb.regTable(line[1:])
                inst += AReg + "\n"
                continue
            elif "KBD" or "SCREEN" in line[1:]:
                AReg = symb.keywordTable(line[1:])
                inst += AReg + "\n"
                continue
        except:
            pass
        try:
            temp1 = int(line[1:])
            if type(temp1) == int: #if its @0-@15 then get from regTable
                if temp1 >= 0 and temp1 <=15:
                    AReg = symb.regTable(line[1:])
                    inst += AReg + "\n"
                    continue
                else:
                    temp1 = format(temp1,"016b") #otherwise if its an int more than 15 then
                    # make its equivalent bin value and update labels
                    labels[line[1:]] = str(temp1) 
                    AReg = str(temp1)
                    inst += AReg + "\n"
                    continue

        except:
            try:
                #if line[1:] in labels:
                temp0 = format(labels[line[1:]],'016b') #if LABEL is in labels then get address
                AReg = str(temp0)
                inst += AReg + "\n"
                continue
            except:
                #then its a variable, create key value for variable using varSpace in runtime and update labels and AReg
                if line[1:] not in labels:
                    temp2 = format(varSpace,'016b')
                    labels[line[1:]] = str(temp2)
                    AReg = str(temp2)
                    varSpace += 1
                elif line[1:] in labels:
                    # temp3 = format(int(labels[line[1:]]),'016b')
                    AReg = labels[line[1:]]
                inst += AReg + "\n"
                continue


        
        
        # try:
        #     temp = int(line[1:])
        #     #assuming its an int
        #     if temp >=0 and temp <=15:
        #         AReg = symb.regTable(line[1:])
        #     else:
        #         varMem = format(varSpace,'016b')
        #         labels[line[1:]] = str(varMem)
        #         AReg = str(varMem)
        #     varSpace +=1
             
        #     inst += AReg + "\n"
        #     continue
        # except:
        #     #for variables
        #     if line[1:] not in labels:
        #         temp = format(varSpace,'016b')
        #         labels[line[1:]] = temp
        #         AReg = str(temp)
        #         inst += AReg + "\n"
        #         continue
            
        #     elif "SCREEN" or "KBD" in line[1:]: 
        #         AReg = symb.keywordTable(line[1:])
        #         inst += AReg + "\n"
        #         continue
        #     elif line[1] == "R":
        #         AReg = symb.regTable(line[1:])
        #         inst += AReg + "\n"
        #         continue

    # print(labels)
    arr = re.split("=|;",line)
    print(arr)
    
    if 'J' in line and 'M' in arr[0]:
        A = "1"
    elif 'J' in line and 'M' not in arr[0]:
        A = "0"
    
    if 'M' in arr[1] and 'J' not in arr[1]:
        A = "1"
    elif 'M' not in arr[1]:
        A = "0"
    
    try:
        if len(arr) == 2 and 'J' in arr[1]:
            jmp = symb.jmpTable(arr[1])
            dest = '000'
            comp = symb.compTable(arr[0])
            inst += C_msb + A + comp + dest + jmp + "\n"
            continue
        
        else: #no jump in the command
            jmp = '000'
            dest = symb.destTable(arr[0])
            comp = symb.compTable(arr[1])
            inst += C_msb + A + comp + dest + jmp + "\n"
            continue
            
    except:
        print("jmp error")
        
    
    if "=" not in line:
        jmp = symb.jmpTable(arr[1])
        dest = "000"
        comp = symb.compTable(arr[0])
        inst += C_msb + comp + dest + jmp + "\n"
        continue

#end of 2nd pass
f.close()
#write the op into the new file
with open("add.hack",'w') as f:
    f.write(inst)

f.close()