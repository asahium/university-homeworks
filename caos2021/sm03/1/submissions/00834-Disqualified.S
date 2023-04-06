#include <sys/syscall.h>
    .global main

write:
    push    %ebp
    mov     %esp, %ebp
    mov     $SYS_write, %eax
    mov     $STDOUT, %ebx
    mov     $1, %edx
    int     $0x80
    mov     %ebp, %esp
    pop     %ebp
    ret

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

main:
    .equ    STDOUT, 1
    .equ    STDIN, 0
    xor     %edi, %edi 
loop:
    mov     $input, %ecx
    call    read
    test    %eax, %eax
    jle     result

    mov     input, %al
    cmp     %al, end
    je      print_end

    inc     %edi
    cmp     $11, %edi
    jne     print_without_end

    mov     $1, %edi
    mov     $end, %ecx
    call    write

print_without_end:
    mov     input, %al
    mov     %al, output
    mov     $input, %ecx
    call    write
    jmp     loop

print_end:
    xor     %edi, %edi
    movb    $0x0a, output
    mov     $output, %ecx
    call    write
    jmp     loop

result:
    cmp     $0x0a, output
    je      return
    mov     $end, %ecx
    call    write

return:
    mov     $SYS_exit, %eax
    mov     $0, %ebx
    int     $0x80

    .data
end:
    .byte   '\n'
input:
    .byte   0
output:
    .byte   '\n'
