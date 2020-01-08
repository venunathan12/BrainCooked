Tmp = open("Template.txt", "r")
T = Tmp.read().split('#')
Tmp.close()

In = open("Compiled.txt", "r")
I = In.readlines()
In.close()

for i in range(len(I)):
    T[63 - i] += I[i]

Out = open("Instruction.txt", "w")
for t in T:
    Out.write(t)
Out.close()