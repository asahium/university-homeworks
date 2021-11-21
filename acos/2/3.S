	.global process
process:
    push %ebp
    mov %esp, %ebp
    mov %esp, %edx
loop:
    call readi32
    jc print

    push %eax
    jmp loop
print:
    cmp %esp, %edx
    je exit

    pop %eax
    call writei32
    jmp print
exit:
    mov %ebp, %esp
    pop %ebp
    ret
