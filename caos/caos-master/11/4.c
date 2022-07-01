#include <asm/unistd.h>

typedef struct FileWriteState
{
    int fd;
    unsigned char *buf;
    int bufsize;
    int filled;
} FileWriteState;

static unsigned char buf[4096];

FileWriteState state = {
        1, buf, 4096, 0
};

FileWriteState *stout = &state;

__attribute__((fastcall)) void flush(FileWriteState *out) {
    volatile int r = 0;

    asm volatile (
        "mov    %1, %%eax\n"
        "mov    %2, %%ebx\n"
        "mov    %3, %%ecx\n"
        "mov    %4, %%edx\n"
        "int    $0x80\n"
        "mov    %%eax, %0\n"
        : "=g"(r)
        : "g"(__NR_write),
        "g"(out->fd),
        "g"((unsigned int)out->buf), "g"(out->filled)
        :
        "eax", "ebx", "ecx", "edx"
    );
}

__attribute__((fastcall)) void writechar(int c, FileWriteState *out) {
    if (out->filled == out->bufsize) {
        flush(out);
        out->filled = 0;
    }

    out->buf[out->filled++] = c;
}
