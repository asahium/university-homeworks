#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    char * out = argv[1];

    char name[L_tmpnam] = {"asdasdasd.c"};

    char ext_out[strlen(out) + 2];
    strcpy(ext_out, "./");
    strcat(ext_out + 2, out);

    char compiler_name[20] = {"gcc"};

    FILE *f = fdopen(creat(name, 0777), "w");

    fprintf(f,  "#include <stdio.h>\n\n"
                "int main() {\n"
                "    long long m;\n"
                "    scanf(\"%%lld\", &m);\n"
                "    printf(\"%%lld\", (m * (m + 1) / 2) %% %s);\n"
                "}", argv[2]);

    fflush(f);
    fclose(f);

    if (!fork()) {
        execlp(compiler_name, compiler_name, name, "-o", out, NULL);
        _exit(0);
    }

    waitpid(-1, NULL, 0);

    chmod(out, 0751);

    if (!fork()) {
        execlp("rm", "rm", name, NULL);
        _exit(0);
    }

    waitpid(-1, NULL, 0);
}