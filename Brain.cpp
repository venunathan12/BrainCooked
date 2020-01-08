#include <stdio.h>

#include <iostream>

using namespace std;

unsigned int Space[4096];
char InsC[4096];
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

    InsPoint = 0; Point = 0;
    while (InsPoint < 4096)
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
        }
        
        default:
            break;
        }

        InsPoint ++;
    }

    for(int I = 0; I < 16; I++)
        cout << Space[I] << "   ";    

    fclose(Ins); fclose(Inp); fclose(Out);
    return 0;
}