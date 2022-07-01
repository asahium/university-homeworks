/* Взято с семинара 194 группы */
#include <sys/mman.h>
#include <stdlib.h>
#include <sys/eventfd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>

enum {STR_LEN = 4096};

void incr(char *str, unsigned base) {
    int l = strlen(str);
    for(int i = 0; i < l; ++i){
        if (str[i] == '0' + base - 1){
            str[i] = '0';
        } else {
            str[i]++;
            return;
        }
    }
    str[l] = '1';
}

void proc(int proc_num, int fd_this, int fd_other,
          unsigned max_iter, char *str, unsigned base)
{
    while (1) {
        unsigned long long val;
        read(fd_this, &val, sizeof(val));
        if (val > max_iter) {
            _exit(0);
        }
        ++val;
        printf("%d %s\n", proc_num, str); fflush(stdout);
        incr(str, base);
        write(fd_other, &val, sizeof(val));
        if (val >= max_iter) {
            _exit(0);
        }
    }
}

int main(int argc, char **argv) {
    unsigned long N = strtoll(argv[1], NULL, 0);
    if (!N) {
        printf("Done\n"); fflush(stdout);
        return 0;
    }
    unsigned K = strtol(argv[2], NULL, 0);

    char *str = mmap(NULL, STR_LEN, PROT_READ | PROT_WRITE,
                     MAP_SHARED|MAP_ANONYMOUS, -1, 0);
    if (str == MAP_FAILED) {
        return 1;
    }
    strcpy(str, argv[3]);

    int fd1 = eventfd(1, 0);
    int fd2 = eventfd(0, 0);

    if (!fork()) {
        proc(1, fd1, fd2, N, str, K);
    }

    if (!fork()) {
        proc(2, fd2, fd1, N, str, K);
    }
    munmap(str, STR_LEN);
    close(fd1);
    close(fd2);
    wait(NULL);
    wait(NULL);
    printf("Done\n"); fflush(stdout);

    return 0;
}
