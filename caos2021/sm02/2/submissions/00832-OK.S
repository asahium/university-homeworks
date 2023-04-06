    .global list_reverse
list_reverse:
    push    %ebp
    mov     %esp, %ebp
    xor     %eax, %eax
    mov     head, %edx
reverse_loop:
    test    %edx, %edx
    jz      end_loop

    mov     8(%edx), %ecx
    mov     %eax, 8(%edx)

    mov     %edx, %eax
    mov     %ecx, %edx
    jmp     reverse_loop
end_loop:
    mov     %eax, head
    mov     %ebp, %esp
    pop     %ebp
    ret
