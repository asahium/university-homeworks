        .text
zero:   .double 0.0
one:    .double 1.0
mone:   .double -1.0
        .global myexpm2
myexpm2:
        push    %ebp
        mov     %esp, %ebp
        push    %ebx

        andl    $0xfffffff0, %esp

        movsd   zero, %xmm0
        movsd   zero, %xmm1

        movsd   8(%ebp), %xmm2 
        mulsd   %xmm2, %xmm2

        movsd   one, %xmm3
        movsd   zero, %xmm4

loop:   
        addsd   %xmm3, %xmm1

        comisd  %xmm1, %xmm0
        jz      fin

        movsd   %xmm1, %xmm0
        mulsd   %xmm2, %xmm3

        addsd   one, %xmm4

        divsd   %xmm4, %xmm3
        mulsd   mone, %xmm3

        jmp     loop
fin:
        movl    16(%ebp), %ecx

        sub     $8, %esp
        movsd   %xmm0, (%esp)

        movl    (%esp), %eax
        movl    %eax, (%ecx)

        movl    4(%esp), %eax
        movl    %eax, 4(%ecx)
        
        add     $8, %esp

        mov     %ebp, %esp
        subl    $12, %esp

        pop     %ebx
        pop     %ebp
        ret