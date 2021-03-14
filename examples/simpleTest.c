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