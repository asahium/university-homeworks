#include <math.h>
#include <stdio.h>
#include <string.h>

typedef double (*funcptr_t)(double a);

typedef struct FunctionTable
{
    funcptr_t func;
    char * name;
} FTable;

static const FTable table[] = {
        { &sin, "sin" },
        { &cos, "cos" },
        { &exp, "exp" },
        { &log, "log" },
        { &tan, "tan" },
        { &sqrt, "sqrt"}
};

int main() {
    char name[1000000];
    double num;

    size_t i;

    while (scanf("%s %lg", name, &num) == 2) {
        int f = 0;
        for (i = 0; i < sizeof(table) / sizeof(FTable); ++i) {
            if (!strcmp(table[i].name, name)) {
                printf("%a\n", table[i].func(num));
                f = 1;
                break;
            }
        }

        if (!f)
            printf("%a\n", NAN);
    }
}