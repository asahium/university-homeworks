    .text
    .global dot_product
dot_product:
    push    %ebp
    movl    %esp, %ebp

    movl    8(%ebp), %eax
    movl    12(%ebp), %ecx
    movl    16(%ebp), %edx

    pxor    %xmm0, %xmm0
itv:
    cmpl    $4, %eax
    jl      itve

    movups  (%ecx), %xmm1
    movups  (%edx), %xmm2

    mulps   %xmm2, %xmm1
        
    haddps  %xmm1, %xmm0

    sub     $4, %eax
    add     $16, %ecx
    add     $16, %edx

    jmp     itv
itve:
    pxor    %xmm1, %xmm1

    haddps  %xmm1, %xmm0
    haddps  %xmm1, %xmm0
its:
    cmpl    $0, %eax
    je      itse

    movss   (%ecx), %xmm1
    movss   (%edx), %xmm2

    mulss   %xmm2, %xmm1

    addss   %xmm1, %xmm0

    add     $4, %ecx
    add     $4, %edx

    dec     %eax

    jmp     its
itse:
    subl    $4, %esp

    movss   %xmm0, (%esp)

    flds    (%esp)

    addl    $4, %esp

    leave
    ret
