#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    char name[L_tmpnam] = {"asdasdasd.c"};
    char compiled[L_tmpnam] = {"dasdvdfd"};
    char ext_compiled[L_tmpnam + 2] = {"./dasdvdfd"};

    char compiler_name[20] = {"gcc"};

    printf("%s %s %s", name, compiled, ext_compiled);

    FILE *f = fdopen(creat(name, 0644), "w");

    fprintf(f, "#include <math.h>\n"
               "#include <stdio.h>\n"
               "long double f(long double x) {\nreturn %s;\n }\n"
               "int main() {\n"
               "long double z;\n"
               "while (scanf(\"%%Lf\", &z) == 1) {\n"
               "printf(\"%%.10g\\n\", (long double)f(z));\n}\n}\n", argv[1]);

    fflush(f);
    fclose(f);

    if (!fork()) {
        execlp(compiler_name, compiler_name,
                name, "-o", compiled, "-lm", NULL);
        _exit(0);
    }

    waitpid(-1, NULL, 0);

    if (!fork()) {
        execl(ext_compiled, "", NULL);
        _exit(0);
    }

    waitpid(-1, NULL, 0);

    if (!fork()) {
        execlp("rm", "rm", name, compiled, NULL);
        _exit(0);
    }

    waitpid(-1, NULL, 0);
}