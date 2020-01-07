from Assembler import BrainNode

Code = []
FnMap = {}; FnData = {}
VarMap = {}

def BreakDown():
    
    ActiveFn = None
    for C in Code:
        Cs = C.split(' ')

        T = Cs.pop(0)
        if T == "func":
            X = Cs.pop(0)
            ActiveFn = X

            L = FnMap[X] = len(FnMap.keys())
            FnData[L] = []
            VarMap[L] = [{}, 0]

        elif T == "endfunc":
            ActiveFn = None

        elif T == "int":
            X = Cs.pop(0)

            L = FnMap[ActiveFn]
            VarMap[L][0][X] = VarMap[L][1]; VarMap[L][1] += 1

        elif T == "str":
            pass

        else:
            if T in VarMap[FnMap[ActiveFn]][0].keys():
                X = Cs.pop(0)

                if X == "set":
                    FnData[FnMap[ActiveFn]].append(['SET', VarMap[FnMap[ActiveFn]][0][T], Cs.pop(0)])
                    
                elif X == "=":
                    Y = Cs.pop(0)

                    if Y in VarMap[FnMap[ActiveFn]][0].keys():
                        FnData[FnMap[ActiveFn]].append(['COPY', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][0][Y]])
                
                elif X == "<-":
                    Y = Cs.pop(0)

                    if Y in VarMap[FnMap[ActiveFn]][0].keys():
                        FnData[FnMap[ActiveFn]].append(['MOVE', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][0][Y]])

    FnData[0].append(['END'])

def Assemble():

    Fns = []

    I = 0
    while I in FnData.keys():
        Fns.append([])
        ExeLine = 0

        for Op in FnData[I]:
            X = Op.pop(0)
            Command = ""
            B = BrainNode(VarMap[I][1])

            if X == "SET":
                Targ = Op.pop(0)
                Val = Op.pop(0)

                if Val[0] == '"':
                    pass
                else:
                    Val = int(Val)
                    Command += B.AccessLocal(Targ)
                    Command += B.ModifyLocal(Val)
                    Command += B.ReturnToBase()

                    Command += B.ChangeExeLine(ExeLine, ExeLine+1)
                    Command += B.ParkOutside()

            elif X == "END":
                Command += B.MovePtr(2 - B.ReturnDist)
                Command += B.ModifyLocal(-1)
                Command += B.ReturnToBase()
                Command += B.ParkOutside()
            
            elif X == "COPY":
                Targ = Op.pop(0)
                From = Op.pop(0)
                
                Loop = B.ForPositive()
                Command += B.AccessLocal(From)
                Command += Loop[0]
                Command += B.ReturnToBase() + B.ModifyLocal(1)
                Command += B.AccessLocal(Targ) + B.ModifyLocal(1) + B.ReturnToBase() + B.AccessLocal(From)
                Command += Loop[1]
                Command += B.ReturnToBase()
                Command += Loop[0]
                Command += B.AccessLocal(From) + B.ModifyLocal(1) + B.ReturnToBase()
                Command += Loop[1]

                Command += B.ChangeExeLine(ExeLine, ExeLine+1)
                Command += B.ParkOutside()
            
            elif X == "MOVE":
                Targ = Op.pop(0)
                From = Op.pop(0)

                Loop = B.ForPositive()
                Command += B.AccessLocal(From)
                Command += Loop[0]
                Command += B.ReturnToBase() + B.AccessLocal(Targ) + B.ModifyLocal(1)
                Command += B.ReturnToBase() + B.AccessLocal(From)
                Command += Loop[1]
                Command += B.ReturnToBase()

                Command += B.ChangeExeLine(ExeLine, ExeLine+1)
                Command += B.ParkOutside()

            Fns[-1].append(Command)
            ExeLine += 1

        I += 1
    
    return Fns

if __name__ == "__main__":
    
    Source = open("Source.pc", "r")

    Code = Source.readlines()
    for I in range(len(Code)):
        Code[I] = Code[I].split('\n')[0]
    Source.close()

    Ln = len(Code)
    I = 0
    while I < Ln:
        if Code[I] == "":
            Ln -= 1
            Code.pop(I)
        else:
            I += 1

    BreakDown()
    print(FnData)
    print(Assemble())