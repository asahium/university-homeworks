// Total tests: 6
// Failed tests:
// 5 - Wrong answer



#include <sys/syscall.h>

    .global mul2
mul2:
    push %ebp
    mov %esp, %ebp
    xor %ecx, %ecx
    add $1, %ecx
    shl $31, %ecx
    sub $1, %ecx
    shr $1, %ecx
    movl 8(%ebp), %eax
    cmpl %ecx, (%eax)
    jg not_end
end:
    movl (%eax), %ecx
    shl $1, %ecx
    movl %ecx, (%eax)
not_end:
    mov %ebp, %esp
    pop %ebp
    ret

.data
