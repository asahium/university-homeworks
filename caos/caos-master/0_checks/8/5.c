#include <dlfcn.h>
#include <fcntl.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (!fork()) {
        int fd = open("mylib.c", O_CREAT | O_TRUNC| O_RDWR, 0777);
        FILE *f = fdopen(fd, "w");
        fprintf(f, "#define _USE_MATH_DEFINES\n"
                    "#include <math.h>\n"
                    "double func(double x) {\n"
                    "return %s;\n}\n", argv[4]);
        fclose(f);
        execlp("gcc", "gcc", "-DPIC", "-fPIC", "-shared", "-lm", "mylib.c", "-o", "mylib.so", NULL);
        _exit(0);
    }
    waitpid(-1, NULL, 0);
    double left = strtod(argv[1], NULL);
    double right = strtod(argv[2], NULL);
    void* handler = dlopen("./mylib.so", RTLD_LAZY);
    void* func = dlsym(handler, "func");
    int n = atoi(argv[3]);
    double dx = (right - left) / n;
    double result = 0;
    for (int i = 0; i < n; ++i) {
        double x = left + i * dx;
        double res = ((double (*)(double))func)(x) * dx;
        result += res;
    }
    printf("%.10g\n", result);
}