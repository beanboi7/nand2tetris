import re

def parser(line):
    RegA = ""
    Cinst_MSB4 = ""
    dest = ""
    jmp = ""
    comp = ""
    if line[0] == '@':
        RegA = format(int(line[1]),'016b')
        RegA += "\n"
        return RegA
    elif 'M' in line:
        Cinst_MSB4 = "1111"
    
    Cinst_MSB4 = "1110"
    
    arr = line.split()
    if "\n" in arr:
        arr.remove("\n")
    
    deString = ''
    for i in range(len(arr[0])):
        deString = deString + arr[0][i]

    arr = re.split(r"=|;", deString)
    print(arr)

    for word in arr:
        if dest == "":
            bin_ = destTable(word)
            dest += bin_
        elif comp == "":
            bin_ = comptable(word)
            comp += bin_
        elif jmp == "":
            bin_ = jmpTable(word)
            jmp += bin_
    
    if jmp == "":
        jmp = "000"
    final_inst = Cinst_MSB4 + comp + dest + jmp + "\n"
    return final_inst

def comptable(key):
    comp = {
        #comp fields
        "0":"101010",
        "1":"111111",
        "-1":"111010",
        "D":"001100",
        "A":"110000",
        "M":"110000",
        "!D":"001101",
        "!A":"110001",
        "!M":"110001",
        "-D":"001111",
        "-A":"110011",
        "-M":"110011",
        "D+1":"011111",
        "A+1":"110111",
        "M+1":"110111",
        "D-1":"001110",
        "A-1":"110010",
        "M-1":"110010",
        "D+A":"000010",
        "D+M":"000010",
        "D-A":"010011",
        "D-M":"010011",
        "A-D":"000111",
        "M-D":"000111",
        "D&A":"000000",
        "D&M":"000000",
        "D|A":"010101",
        "D|M":"010101",
    }
    return comp[key]

def destTable(key):
    dest = {
        #destination fields
        "M":"001",
        "D":"010",
        "MD":"011",
        "A":"100",
        "AM":"101",
        "AD":"110",
        "AMD":"111",
    }
    return dest[key]

def jmpTable(key):
    jmp = {
        #jmp fields
        "":"000",
        "JGT":"001",
        "JEQ":"010",
        "JGE":"011",
        "JLT":"100",
        "JNE":"101",
        "JLE":"110",
        "JMP":"111",
    }

    return jmp[key]

file = "../add/Add.asm"
f = open(file, "r")
inst = ""
for line in f:
    if line.startswith("//") or line.startswith("\n"):
        continue
    inst += parser(line)

f.close()

with open("add.hack","w") as f:
    f.write(inst)
f.close()

