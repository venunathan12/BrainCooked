#include <stdio.h>

#include <iostream>

using namespace std;

#define INSMEM 1024*64

unsigned int Space[4096];
char InsC[INSMEM];
int InsPoint, Point;

int main()
{
    FILE * Ins = fopen("Instruction.txt", "r");
    FILE * Inp = fopen("Input.txt", "r");
    FILE * Out = fopen("Output.txt", "w");

    InsPoint = 0;
    while(!feof(Ins))
    {
        fscanf(Ins, "%c", &InsC[InsPoint]);
        InsPoint ++;
    }

    cout << "Program Output :" << endl;

    InsPoint = 0; Point = 0;
    while (InsPoint < INSMEM)
    {
        char I = InsC[InsPoint];

        switch (I)
        {
        case '<':
            Point --;
            break;

        case '>':
            Point ++;
            break;

        case '+':
            Space[Point] ++;
            break;
        
        case '-':
            Space[Point] --;
            break;
        
        case '[':
        {
            if (Space[Point] == 0)
            {
                int In = 1;
                while (true)
                {
                    InsPoint ++;
                    if (InsC[InsPoint] == ']')
                        In --;
                    else if(InsC[InsPoint] == '[')
                        In ++;

                    if (In == 0)
                        break;
                }
            }
            break;
        }
        
        case ']':
        {
            if (Space[Point] != 0)
            {
                int In = 1;
                while (true)
                {
                    InsPoint --;
                    if (InsC[InsPoint] == '[')
                        In --;
                    else if(InsC[InsPoint] == ']')
                        In ++;

                    if (In == 0)
                        break;
                }
            }
            break;
        }

        case '.':
            fprintf(Out, "%c", Space[Point]);
            printf("%c", Space[Point]);
            break;
        
        case ',':
            fscanf(Inp, "%c", &Space[Point]);
            break;
        
        default:
            break;
        }

        InsPoint ++;
    }

    cout << endl << endl << endl;
    cout << "First 64 Memory Cells, Displayed Below : " << endl;
    for(int I = 0; I < 64; I++)
        cout << Space[I] << "   ";    

    fclose(Ins); fclose(Inp); fclose(Out);
    return 0;
}