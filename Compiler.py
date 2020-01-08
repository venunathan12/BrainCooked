from Assembler import BrainNode

Code = []
FnMap = {}; FnData = {}
VarMap = {}

IFQueue = []; IFStatus = []

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
        
        elif T == "end":
            FnData[FnMap[ActiveFn]].append(['END'])
        
        elif T == "return":
            Y = Cs.pop(0)

            if Y in VarMap[FnMap[ActiveFn]][0].keys():
                FnData[FnMap[ActiveFn]].append(['RETURN', VarMap[FnMap[ActiveFn]][0][Y]])
        
        elif T == "if":
            Y = Cs.pop(0)

            if Y in VarMap[FnMap[ActiveFn]][0].keys():
                FnData[FnMap[ActiveFn]].append(['IF', VarMap[FnMap[ActiveFn]][0][Y]])

        elif T == "else":
            FnData[FnMap[ActiveFn]].append(['ELSE'])
        
        elif T == "endif":
            FnData[FnMap[ActiveFn]].append(['ENDIF'])

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
                    Y = Cs.pop(0)

                    if Y[0] == '"':
                        pass
                    else:
                        FnData[FnMap[ActiveFn]].append(['CLEAR', VarMap[FnMap[ActiveFn]][0][T]])
                        FnData[FnMap[ActiveFn]].append(['MOD', VarMap[FnMap[ActiveFn]][0][T], Y])
                    
                elif X == "=":
                    Y = Cs.pop(0)

                    if Y in VarMap[FnMap[ActiveFn]][0].keys():
                        FnData[FnMap[ActiveFn]].append(['CLEAR', VarMap[FnMap[ActiveFn]][0][T]])
                        FnData[FnMap[ActiveFn]].append(['COPY', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][0][Y]])
                
                elif X == "<-":
                    Y = Cs.pop(0)

                    if Y in VarMap[FnMap[ActiveFn]][0].keys():
                        FnData[FnMap[ActiveFn]].append(['MOVE', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][0][Y]])

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
            APPEND = True

            if X == "CLEAR":
                Targ = Op.pop(0)

                Loop = B.ForPositive()
                Command += B.AccessLocal(Targ)
                Command += Loop[0] + Loop[1]
                Command += B.ReturnToBase()

                Command += B.ChangeExeLine(ExeLine, ExeLine + 1)
                Command += B.ParkOutside()

            elif X == "MOD":
                Targ = Op.pop(0)
                Val = Op.pop(0)

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
            
            elif X == "IF":
                Trig = Op.pop(0)

                Loop = B.ForPositive()

                Command += B.AccessLocal(Trig)
                Command += Loop[0]
                Command += B.ReturnToBase() + B.ModifyLocal(1) + B.ParkOutside() + B.ModifyLocal(1)
                Command += B.ReturnToBase() + B.AccessLocal(Trig)
                Command += Loop[1]
                Command += B.ReturnToBase()

                Command += Loop[0]
                Command += B.AccessLocal(Trig) + B.ModifyLocal(1) + B.ReturnToBase()
                Command += Loop[1]

                LoopW = B.WhilePositive()

                Command += B.ParkOutside() + B.MovePtr(1) + B.ModifyLocal(1) + B.MovePtr(-1)
                Command += LoopW[0]
                Command += Loop[0] + Loop[1] + B.MovePtr(1)
                Command += Loop[0] + B.ReturnToBase() + B.ChangeExeLine(ExeLine, ExeLine + 1) + B.ParkOutside() + Loop[1]
                Command += LoopW[1]
                Command += B.MovePtr(1)
                Command += Loop[0] + B.ReturnToBase() + "$" + B.ParkOutside() +  Loop[1]

                IFQueue.append(ExeLine)
                IFStatus.append('IF')

            elif X == "ELSE":

                Copy = Fns[-1][IFQueue[-1]].split('$')
                Fns[-1][IFQueue[-1]] = Copy[0] + B.ChangeExeLine(IFQueue[-1], ExeLine) + Copy[1]

                _ = B.ParkOutside()
                Fns[-1][-1] += B.ReturnToBase() + "$" + B.ParkOutside()

                IFQueue[-1] = ExeLine - 1
                IFStatus[-1] = 'ELSE'
                ExeLine -= 1
                APPEND = False

            elif X == "ENDIF":
                Targ = IFQueue.pop(); Status = IFStatus.pop()

                Copy = Fns[-1][Targ].split('$')

                if Status == 'IF':
                    Fns[-1][Targ] = Copy[0] + B.ChangeExeLine(Targ, ExeLine) + Copy[1]
                elif Status == 'ELSE':
                    Fns[-1][Targ] = Copy[0] + B.ChangeExeLine(Targ + 1, ExeLine) + Copy[1]

                Command += B.ChangeExeLine(ExeLine, ExeLine+1)
                Command += B.ParkOutside()
            
            elif X == "RETURN":
                Val = Op.pop(0)

                Loop = B.ForPositive()
                Command += B.AccessLocal(Val)
                Command += Loop[0]
                Command += B.ReturnToBase() + B.ToReturn() + B.ModifyLocal(1)
                Command += B.ReturnToBase() + B.AccessLocal(Val)
                Command += Loop[1]
                Command += B.ReturnToBase()

                Command += B.ToReturn()
                Command += B.MovePtr(1) + B.ModifyLocal(1)
                Command += (B.MovePtr(1) + Loop[0] + Loop[1]) * (B.ReturnDist + B.PAD + B.Sz)
            
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

            if APPEND:
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

    Ps = Assemble()
    Out = open("Compiled.txt", "w")
    for P in Ps:
        for p in P:
            print('\t' + p)
            Out.write(p + '\n')
    Out.close()