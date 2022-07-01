#include <stdio.h>
#include <syscall.h>

struct FileReadState
{
    int fd;
    unsigned char *buf;
    int bufsize;
    int lc;
    int processed;
    int it;
};

unsigned char buf[4 * 1024];

struct FileReadState state = {
        0, buf, 4 * 1024, 0, 0, 0
};

struct FileReadState *stin = &state;

int lastchar() {
    return stin->lc;
}

int nextchar() {
    if (stin->lc == -1)
        return -1;

    int u = 0;

    if (stin->it == stin->processed) {
        if (stin->processed == stin->bufsize) {
            stin->it = 0;
            stin->processed = 0;
        }

        asm volatile(
            "mov %1, %%eax\n"
            "mov %2, %%ebx\n"
            "mov %3, %%ecx\n"
            "mov %4, %%edx\n"
            "int $0x80\n"
            "mov %%eax, %0\n"
        : "=g"(u)
        : "g" (__NR_read), "g" (0), "g" (stin->buf + stin->processed), "g" (stin->bufsize - stin->processed)
        : "%eax", "%ebx", "%ecx", "%edx", "memory"
        );

        if (u > 0) {
            stin->processed += u;
        } else {
            stin->lc = -1;
            return stin->lc;
        }
    }

    stin->lc = stin->buf[stin->it++];

    return stin->lc;
}