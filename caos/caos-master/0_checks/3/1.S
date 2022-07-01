        .data
A:      .int    0
B:      .int    0
C:      .int    0
        .text
        .global process, A, B, C
process:
        pushl   %ebp
        movl    %esp, %ebp
        movl    A, %eax
        mull    X
        movl    %eax, %ecx
        movl    $2, %eax
        mull    B
        subl    %eax, %ecx
        movl    %ecx, %eax
        mull    X
        mull    X
        addl    C, %eax
        popl    %ebp
        ret
