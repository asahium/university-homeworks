        .data
A:      .int    0
B:      .int    0
C:      .int    0
D:      .int    0
R:      .int    0
        .text
        .global A, B, C, D, R
        .global process
process:
        movl    A, %eax
        imull   B
        mov     %eax, R
        mov     C, %eax
        imull   D
        subl    %eax, R
        
