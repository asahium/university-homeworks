        .text
        .global dot_product
dot_product:
        push    %ebp
        movl    %esp, %ebp

        movl    8(%ebp), %eax //n
        movl    12(%ebp), %ecx // *a
        movl    16(%ebp), %edx // * b

        pxor    %xmm0, %xmm0
it_v:
        cmpl    $4, %eax
        jl      it_v_e

        movups  (%ecx), %xmm1
        movups  (%edx), %xmm2

        mulps   %xmm2, %xmm1
        
        haddps  %xmm1, %xmm0 //0 += 1 * 2

        sub     $4, %eax
        add     $16, %ecx
        add     $16, %edx

        jmp     it_v
it_v_e:
        pxor    %xmm1, %xmm1

        haddps  %xmm1, %xmm0
        haddps  %xmm1, %xmm0
it_s:
        cmpl    $0, %eax
        je      it_s_e

        movss   (%ecx), %xmm1
        movss   (%edx), %xmm2

        mulss   %xmm2, %xmm1

        addss   %xmm1, %xmm0

        add     $4, %ecx
        add     $4, %edx

        dec     %eax

        jmp     it_s
it_s_e:
        subl    $4, %esp

        movss   %xmm0, (%esp)

        flds    (%esp)

        addl    $4, %esp

        leave
        ret