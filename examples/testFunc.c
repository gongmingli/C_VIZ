#include <stdio.h>

int testStruct()
{
    int a = 10;
    // #cond "a > 0"
    if(a > 0) {
        // #action "do something"
    } else {
        // #action "do others"
    }
}

void TestFunction(void)
{
    int a;
    a = 0;

    // #cond "a >= 5"
    if(5 <= a) 
    {
        // #action "do a>= 5"
        // #cond "a == 5"
        if(5 == a) 
        {
            // #action "do a == 5"
        } else {
            // #cond "a == 7"
            if(7 == a) 
            {
                // #action "do a==7"
            } else {
                // #action "do other a"
            }
        }
    } else 
    {
        // #action "do a < 5"
        // #cond "deal with a"
        switch(a) {
            case 1:
            case 2:
                // #action "do a == 1/2"
                break;
            default:
                // #action "do other a(3/4)"
                break;
        }
    }
}