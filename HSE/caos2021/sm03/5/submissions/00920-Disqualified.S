#include <sys/syscall.h>
    .global main
write:
    push    %ebp
    mov     %esp, %ebp
    push    %ebx
    mov     $SYS_write, %eax
    mov     $STDOUT, %ebx
    mov     $1, %edx
    mov     $symbol, %ecx
    int     $0x80
    pop     %ebx
    mov     %ebp, %esp
    pop     %ebp
    ret

read:
    push    %ebp
    mov     %esp, %ebp
    push    %ebx
    mov     $SYS_read, %eax
    mov     $STDIN, %ebx
    mov     $symbol, %ecx
    mov     $1, %edx
    int     $0x80
    pop     %ebx
    mov     %ebp, %esp
    pop     %ebp
    ret

find_count:
    push    %ebp
    mov     %esp, %ebp
    mov     symbol, %cl
    mov     $1, %eax
    test    $128, %cl
    jz      zero
    xor     %eax, %eax
    test    $64, %cl
    jz      zero
    inc     %eax

zero:
    mov     %ebp, %esp
    pop     %ebp
    ret

main:
    .equ    STDIN, 0
    .equ    STDOUT, 1
    sub     $4, %esp
    movl    $0, (%esp)

readloop:
    call    read
    test    %eax, %eax
    jz      end
    call    find_count
    add     %eax, (%esp)
    jmp     readloop

end:
    mov     (%esp), %eax
    call    writei32
    add     $4, %esp
    mov     $SYS_exit, %eax
    mov     $0, %ebx
    int     $0x80

    .data
symbol:
    .byte 0
