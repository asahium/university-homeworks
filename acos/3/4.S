#include <sys/syscall.h>

read:
    push    %ebp
    mov     %esp, %ebp
    mov     $SYS_read, %eax
    mov     $STDIN, %ebx
    mov     $1, %edx
    int     $0x80
    mov     %ebp, %esp
    pop     %ebp
    ret

    .global main

main:
    .equ STDIN, 0
    sub     $17, %esp
    movl    $0, 12(%esp)
    movl    $0, 8(%esp)
    movl    $0, 4(%esp)
    movl    $0, (%esp)

readloop:
    mov     %esp, %ecx
    add     $16, %ecx
    call    read
    test    %eax, %eax
    jle     return

    mov     $1, %ecx
    mov     16(%esp), %al
    mov     12(%esp), %edx

    add     %ecx, (%esp)
    cmp     $0x0a, %al
    je      end

    cmp     $0x20, %al
    je      space

    inc     %edx
    mov     %edx, 12(%esp)

    jmp     readloop

space:
    test    %edx, %edx
    jz      sp_no_word
    add     %ecx, 4(%esp)

sp_no_word:
    movl    $0, 12(%esp)
    jmp     readloop

end:
    test    %edx, %edx
    jz      no_word
    add     %ecx, 4(%esp)

no_word:
    add     %ecx, 8(%esp)
    movl    $0, 12(%esp)
    jmp     readloop

return:
    mov     8(%esp), %eax
    call    writei32
    mov     4(%esp), %eax
    call    writei32
    mov     (%esp), %eax
    call    writei32

    add     $17, %esp
    mov     $SYS_exit, %eax
    mov     $0, %ebx
    int     $0x80
