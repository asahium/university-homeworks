void _start() {
    char c = 0;
    int r = 0;

    while (1) {
        asm volatile(
            "mov $3, %%eax\n"
            "mov $0, %%ebx\n"
            "mov %1, %%ecx\n"
            "movl $0, (%%ecx)\n"
            "mov $1, %%edx\n"
            "int $0x80\n"
            "movl %%eax, %0\n"
            : "=g" (r)
            : "g" (&c)
            : "%eax", "%ebx", "%ecx", "%edx", "memory"
        );

        if (!r)
            break;

        c += (c >= 'a' && c <= 'z') * ('A' - 'a');

        asm volatile(
            "mov $4, %%eax\n"
            "mov $1, %%ebx\n"
            "mov %1, %%ecx\n"
            "mov $1, %%edx\n"
            "int $0x80\n"
            "mov %%eax, %0\n"
            : "=g" (r)
            : "g" (&c)
            : "%eax", "%ebx", "%ecx", "%edx", "memory"
        );
    }

    asm volatile(
        "mov $1, %%eax\n"
        "xor %%ebx, %%ebx\n"
        "int $0x80"
        :
        :
        : "%eax", "%ebx"
    );
}