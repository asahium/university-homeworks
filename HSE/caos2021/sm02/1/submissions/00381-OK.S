    .text
    .global A
    .global B
    .global R
    .global process
process:
    pushl %ebp
    movl %esp, %ebp
    xor %ecx, %ecx
    movl A, %eax
    movl $0, R
loop:
    movl $1, %edx
    
    and %eax, %edx 
    cmovnz B, %edx
    shl %cl, %edx
    addl %edx, R

    shr $1, %eax
    addl $1, %ecx
    cmp $32, %ecx
    jl loop

    popl %ebp
    ret
    .data
A:
    .int 0
B:
    .int 0
R:
    .int 0
