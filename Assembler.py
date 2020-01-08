AddrSize = 6

def H_ToBin(In):

    Out = []
    I = 0

    while I < AddrSize:
        Out.append(In % 2)
        In = In // 2

        I += 1
    
    return Out

class BrainNode:

    def __init__(self, Sz = 0):
        self.Pointer = 0
        self.PAD = 1
        self.ReturnDist = AddrSize + 3
        self.Sz = Sz
    
    def ReturnToBase(self):
        P = self.Pointer
        self.Pointer = 0

        if P > 0:
            return "<" * P
        elif P < 0:
            return ">" * (- P)
        else:
            return ""
    
    def AccessLocal(self, I):
        self.Pointer += self.PAD + I
        return ">" * (self.PAD + I)
    
    def ToReturn(self):
        self.Pointer -= self.ReturnDist
        return "<" * self.ReturnDist
    
    def ModifyLocal(self, I):
        if I > 0:
            return "+" * I
        elif I < 0:
            return "-" * (- I)
        else:
            return ""
    
    def ClearLocal(self):
        return "[-]"
    
    def MovePtr(self, X):
        self.Pointer += X
        if X > 0:
            return ">" * X
        if X < 0:
            return "<" * (- X)
        else:
            return ""
    
    def ForPositive(self):
        return "[-", "]"
    
    def WhilePositive(self):
        return "[", "]"
    
    def ChangeExeLine(self, From, To):
        From = H_ToBin(From)
        To = H_ToBin(To)

        Command = ""

        I = 0
        while I < AddrSize:
            Command += self.MovePtr(-1)

            if From[I] != To[I]:
                if From[I] == 0:
                    Command += self.ModifyLocal(1)
                else:
                    Command += self.ModifyLocal(-1)

            I += 1
        Command += self.ReturnToBase()

        return Command
    
    def ParkOutside(self):
        return self.MovePtr(self.PAD + self.Sz)