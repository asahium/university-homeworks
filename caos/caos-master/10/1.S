        .text
pri:    .asciz  "%llu\n"
        .global process
process:
        push    %ebp
        movl    %esp, %ebp
        movq    A, %mm0
        movq    B, %mm1
        psllq   $1, %mm0
        psrlq   $1, %mm1
        psubq   %mm1, %mm0
        subl    $8, %esp
        movq    %mm0, (%esp)
        push    $pri
        call    printf
        movl    %ebp, %esp
        popl    %ebp
        ret