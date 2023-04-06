    .global delegate
delegate:
    push %ebp
    mov %esp, %ebp
    xor %ecx, %ecx
    movl 8(%ebp), %eax
    sub $1, %eax
    movl %eax, %ecx
    shl $2, %ecx
    xor %edx, %edx
    add %ebp, %edx
    add $16, %edx
    add %edx,%ecx
loop:
    cmp %edx, %ecx
    jl end
    push (%ecx)
    sub $4, %ecx
    jmp loop
end:
    movl 12(%ebp), %edx
    call *%edx
    mov %ebp, %esp
    pop %ebp
    ret
.data
