#include <stdio.h>
#include <string.h>
#include <math.h>


typedef double (*funcptr_t)(double a);

typedef struct FunctionTable {
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

int main(void) {
    char *func;
    double x;
    size_t i;
    int check = 0;
    while (scanf("%ms %lg", &func, &x) == 2) {
        check = 0;
        for (i = 0; i < sizeof(table) / sizeof(FTable); ++i) {
            if (!strcmp(table[i].name, func)) {
                printf("%a\n", table[i].func(x));
                check = 1;
                break;
            }
        }
        if (!check) {
            printf("%a\n", NAN);
        }
    }
}