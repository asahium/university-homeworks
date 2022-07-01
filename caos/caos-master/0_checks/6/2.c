#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <string.h>

int main (int argc, char ** argv) {
    float res = atof(argv[1]);

    char * last_lib = argv[2];

    for (int i = 2; i < argc - 1; i += 2) {
        char * lib = argv[i];

        if (strlen(lib) == 1 && *lib == '-') {
            lib = last_lib;
        }

        char * func = argv[i + 1];

        void * lib_obj = dlopen(lib, RTLD_LAZY);

        if (!lib_obj)
            continue;

        void * func_obj = dlsym(lib_obj, func);

        if (!func_obj)
            continue;

        res = ((float(*)(float)) func_obj)(res);

        stpcpy(last_lib, lib);
    }


    printf("%.6g", res);
}

