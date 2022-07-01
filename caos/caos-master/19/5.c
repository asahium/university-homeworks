#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/signalfd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

FILE * in;
FILE * out;

int max;

typedef struct signalfd_siginfo SFDSI;

void process(int child_index) {
    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGUSR1);

    int sig_fd = signalfd(-1, &mask, 0);

    SFDSI sig_data;
    read(sig_fd, &sig_data, sizeof(sig_data));

    int ch2 = 0;
    if (sig_data.ssi_signo == SIGUSR1)
        fscanf(in, "%d", &ch2);

    if (child_index) {
        fprintf(out, "1 ");
    } else {
        fprintf(out, "%d ", getpid());
    }

    fflush(out);

    kill(ch2, SIGUSR1);

    int i = 0;

    while (i < max) {
        read(sig_fd, &sig_data, sizeof(sig_data));

        if (sig_data.ssi_signo != SIGUSR1 ||
            sig_data.ssi_pid != ch2)
            continue;

        fscanf(in, "%d", &i);

        if (i > max)
            break;

        fprintf(stdout, "%d %d\n", child_index + 1, i);
        fflush(stdout);

        fprintf(out, "%d\n", ++i);
        fflush(out);

        kill(ch2, SIGUSR1);
    }

    fclose(in);
    fclose(out);

    _exit(0);
}

int main(int argc, char **argv) {
    sigset_t current;
    sigemptyset(&current);
    sigaddset(&current, SIGUSR1);
    sigprocmask(SIG_BLOCK, &current, NULL);

    max = atoi(argv[1]);
    int fd[2];

    pipe(fd);

    in = fdopen(fd[0], "r");
    out = fdopen(fd[1], "w");

    pid_t pid1 = fork();

    if (!pid1)
        process(0);

    pid_t pid2 = fork();

    if (!pid2)
        process(1);

    fprintf(out, "%d\n", pid2);
    fflush(out);

    kill(pid1, SIGUSR1);

    waitpid(pid1, NULL, 0);
    waitpid(pid2, NULL, 0);

    fclose(in);
    fclose(out);
}