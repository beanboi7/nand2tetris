from hackparser import *

file = "../add/Add.asm"
f = open(file, "r")
inst = ""
for line in f:
    if line.startswith("//") or line.startswith("\n"):
        continue
    inst += hackparser(line)

f.close()

with open("add.hack","w") as f:
    f.write(inst)
f.close()

