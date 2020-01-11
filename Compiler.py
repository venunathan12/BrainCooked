from Assembler import BrainNode

Code = []
FnMap = {}; FnData = {}
VarMap = {}

IFQueue = []; IFStatus = []
WHILEQueue = []
CallInfo = {}

def BreakDown():
    
    ActiveFn = None

    for C in Code:
        Cs = C.split(' ')

        T = Cs[0]
        if T == "func":
            X = Cs[1]
            L = FnMap[X] = len(FnMap.keys())
            FnData[L] = [['FUNC', X]]
            VarMap[L] = [{}, 0]
            CallInfo[X] = [None, []]

    for C in Code:
        Cs = C.split(' ')

        T = Cs.pop(0)
        if T == "func":
            X = Cs.pop(0)
            ActiveFn = X

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
        
        elif T == "while":
            Y = Cs.pop(0)

            if Y in VarMap[FnMap[ActiveFn]][0].keys():
                FnData[FnMap[ActiveFn]].append(['WHILE', VarMap[FnMap[ActiveFn]][0][Y]])

        elif T == "endwhile":
            FnData[FnMap[ActiveFn]].append(['ENDWHILE'])

        elif T == "int":
            while len(Cs):
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
                
                elif X == "rawinput":
                    FnData[FnMap[ActiveFn]].append(['RIN', VarMap[FnMap[ActiveFn]][0][T]])

                elif X == "rawoutput":
                    FnData[FnMap[ActiveFn]].append(['ROUT', VarMap[FnMap[ActiveFn]][0][T]])
                    
                elif X == "=":
                    Y = Cs.pop(0)

                    if Y in VarMap[FnMap[ActiveFn]][0].keys():
                        FnData[FnMap[ActiveFn]].append(['CLEAR', VarMap[FnMap[ActiveFn]][0][T]])
                        FnData[FnMap[ActiveFn]].append(['COPY', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][0][Y]])
                    if Y in FnMap.keys():
                        Action = ['CALL', Y]
                        while len(Cs):
                            R = Cs.pop(0)
                            Action.append(VarMap[FnMap[ActiveFn]][0][R])
                        FnData[FnMap[ActiveFn]].append(Action)

                        FnData[FnMap[ActiveFn]].append(['CLEAR', VarMap[FnMap[ActiveFn]][0][T]])
                        FnData[FnMap[ActiveFn]].append(['MOVE', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][1], 1])

                
                elif X == "<-":
                    Y = Cs.pop(0)
                    H = 1
                    if len(Cs):
                        H = int(Cs.pop(0))

                    if Y in VarMap[FnMap[ActiveFn]][0].keys():
                        FnData[FnMap[ActiveFn]].append(['MOVE', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][0][Y], H])
                
                elif X == "-=":
                    Y = Cs.pop(0)

                    if Y in VarMap[FnMap[ActiveFn]][0].keys():
                        FnData[FnMap[ActiveFn]].append(['CDCR', VarMap[FnMap[ActiveFn]][0][T], VarMap[FnMap[ActiveFn]][0][Y]])

def Assemble():

    Fns = []; Fns.append([])

    I = 0
    ExeLine = 0

    while I in FnData.keys():

        for Op in FnData[I]:
            X = Op.pop(0)
            Command = ""
            B = BrainNode(VarMap[I][1] + 1)
            APPEND = True

            if X == "FUNC":
                Val = Op.pop(0)
                CallInfo[Val][0] = ExeLine

                for R in CallInfo[Val][1]:
                    Copy = Fns[-1][R].split('$')
                    Fns[-1][R] = Copy[0] + B.ChangeExeLine(0, ExeLine) + Copy[1]

                ExeLine -= 1
                APPEND = False
            
            if X == "CALL":
                Fn = Op.pop(0)

                Args = []
                while len(Op):
                    Args.append(Op.pop(0))
                
                Loop = B.ForPositive()

                Command += B.ParkOutside() + B.ModifyLocal(-1) + B.MovePtr(1) + B.ModifyLocal(1) + B.MovePtr(-2)
                Command += B.MovePtr(B.ReturnDist)
                if CallInfo[Fn][0] == None:
                    Command += "$"
                    CallInfo[Fn][1].append(ExeLine)
                else:
                    Command += B.ChangeExeLine(0, CallInfo[Fn][0])
                Command += B.ReturnToBase()
                Command += B.ChangeExeLine(ExeLine, ExeLine + 1)

                Item = 0
                for A in Args:
                    Command += B.AccessLocal(A)
                    Command += Loop[0]
                    Command += B.ReturnToBase() + B.ModifyLocal(1) + B.ParkOutside() + B.MovePtr(B.ReturnDist - 1) + B.AccessLocal(Item) + B.ModifyLocal(1)
                    Command += B.ReturnToBase() + B.AccessLocal(A)
                    Command += Loop[1]
                    Command += B.ReturnToBase()
                    Command += Loop[0]
                    Command += B.AccessLocal(A) + B.ModifyLocal(1) + B.ReturnToBase()
                    Command += Loop[1]

                    Item += 1
                
                Command += B.ParkOutside()
                Command += B.MovePtr(B.ReturnDist + Item + B.PAD)
            
            elif X == "CLEAR":
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
            
            elif X == "WHILE":
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

                WHILEQueue.append(ExeLine)

            elif X == "ENDWHILE":

                W = WHILEQueue.pop()
                Copy = Fns[-1][W].split('$')
                Fns[-1][W] = Copy[0] + B.ChangeExeLine(W, ExeLine + 1) + Copy[1]                

                Command += B.ChangeExeLine(ExeLine, W)
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
                Incr = Op.pop(0)

                Loop = B.ForPositive()
                Command += B.AccessLocal(From)
                Command += Loop[0]
                Command += B.ReturnToBase() + B.AccessLocal(Targ) + B.ModifyLocal(Incr)
                Command += B.ReturnToBase() + B.AccessLocal(From)
                Command += Loop[1]
                Command += B.ReturnToBase()

                Command += B.ChangeExeLine(ExeLine, ExeLine+1)
                Command += B.ParkOutside()
            
            elif X == "CDCR":
                Targ = Op.pop(0)
                Sub = Op.pop(0)
                
                Loop = B.ForPositive(); LoopW = B.WhilePositive()
                Command += B.ChangeExeLine(ExeLine, ExeLine+1) 

                Dist = Sub - Targ
                if Dist > 0:
                    Command += B.AccessLocal(Targ)
                    Command += LoopW[0]
                    Command += B.MovePtr(Dist)
                    Command += Loop[0] + B.MovePtr(-Dist) + B.ModifyLocal(-1) + B.MovePtr(-(Targ + B.PAD)) + Loop[1] + B.MovePtr(Targ + B.PAD)
                    Command += LoopW[1] + B.ParkOutside()
            
            elif X == "RIN":
                Targ = Op.pop(0)

                Command += B.AccessLocal(Targ) + B.RawInput() + B.ReturnToBase()
                Command += B.ChangeExeLine(ExeLine, ExeLine+1)
                Command += B.ParkOutside()
            
            elif X == "ROUT":
                Targ = Op.pop(0)

                Command += B.AccessLocal(Targ) + B.RawPrint() + B.ReturnToBase()
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
        Code[I] = Code[I].split('\n')[0].split('\t')[-1]
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
    print(CallInfo)

    Out = open("Compiled.txt", "w")
    for P in Ps:
        for p in P:
            print('\t' + p)
            Out.write(p + '\n')
    Out.close()