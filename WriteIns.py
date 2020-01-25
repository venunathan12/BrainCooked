AddrSize = 8

Tmp = open("Template.txt", "r")
T = Tmp.read().split('#')
Tmp.close()

In = open("Compiled.txt", "r")
I = In.readlines()
In.close()

print(f"{len(I)} Instructions will be written.")
if len(I) > 2**AddrSize:
    print("Too many INS.")
    exit()

for i in range(len(I)):
    T[2**AddrSize - 1 - i] += I[i]

Out = open("Instruction.txt", "w")
for t in T:
    Out.write(t)
Out.close()