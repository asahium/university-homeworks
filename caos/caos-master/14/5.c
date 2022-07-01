#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    unsigned char bytes[64];
} ARGS;

ARGS write(int argc, char **argv) {
    ARGS out;

    int os = 0;
    int in;
    double d;

    for (int i = 4; i < argc; ++i) {
        char m = argv[3][i - 3];

        if (m == 'i') {
            in = atoi(argv[i]);
            memcpy(out.bytes + os, &in, sizeof(int));
            os += sizeof(int);
        } else if (m == 'd') {
            d = strtod(argv[i], NULL);
            memcpy(out.bytes + os, &d, sizeof(double));
            os += sizeof(double);
        } else if (m == 's') {
            memcpy(out.bytes + os, argv + i, sizeof(char*));
            os += sizeof(char*);
        }
    }

    return out;
}


int main(int argc, char **argv) {
    void * lib = dlopen(argv[1], RTLD_LAZY);
    void * func = dlsym(lib, argv[2]);

    ARGS f_args = write(argc, argv);
    char r = argv[3][0];

    if (r == 'i')
        printf("%d\n", ((int (*)(ARGS))func)(f_args));
    else if (r == 'd')
        printf("%.10g\n", ((double (*)(ARGS))func)(f_args));
    else if (r == 's')
        printf("%s\n", ((char *(*)(ARGS))func)(f_args));
    else
        ((void (*)(ARGS))func)(f_args);

    dlclose(lib);
}