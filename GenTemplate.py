AddrSize = 8

Out = open("Template.txt", "w")

Out.write(">->+\n[>\n" + ">" * AddrSize + "+" + "<" * AddrSize + "\n\n")

def Mark(C, L):
    if C == L:
        Out.write("\t" * 0 + "[-\n")
        Out.write("\t" * 0 + "#\n")
        Out.write("\t" * 0 + "]\n")
        return
    
    Out.write("\t" * 0 + "[>\n")
    Mark(C+1, L)
    Out.write("\t" * 0 + "]>\n")
    Mark(C+1, L)

Mark(0,AddrSize)

Out.write("+[-<+]-\n>]")

Out.close()