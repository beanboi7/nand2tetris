import re
from symboltable import *

def code(line):
    symb = SymbolTable()
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
            bin_ = symb.destTable(word)
            dest += bin_
        elif comp == "":
            bin_ = symb.compTable(word)
            comp += bin_
        elif jmp == "":
            bin_ = symb.jmpTable(word)
            jmp += bin_
    
    if jmp == "":
        jmp = "000"
    final_inst = Cinst_MSB4 + comp + dest + jmp + "\n"
    return final_inst