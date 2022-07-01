//void __init_mem() {}
void __init_stdin() {}
void __init_stdout() {}

void __fini_mem() {}
void __fini_stdin() {}
void __fini_stdout() {}

void _exit(int status) __attribute__((noreturn));
void exit(int status) __attribute__((noreturn));

int strlen(const char* const str)
{
    const char* it = str;
    while (*it) ++it;
    return it - str;
}

int write_stdout(const char* const str)
{
    int len = strlen(str);
    int res;
    __asm__ volatile(
    "int    $0x80\n\t"
    :"=a"(res)
    :"a"(4),"b"(1),"c"(str),"d"(len)
    );
    return res;
}

int main(int argc, char** argv, char** env)
{
    for (int i = 0; i < argc; ++i) {
        write_stdout(argv[i]);
        write_stdout("\n");
    }
    int i = 0;
    while (env[i]) {
        write_stdout(env[i++]);
        write_stdout("\n");
    }
}