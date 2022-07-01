        .text
        .global satsum

satsum:
        pushl   %ebp
        movl    %esp, %ebp
        movl    8(%ebp), %eax
        addl    12(%ebp), %eax

        jnc     finish
        movl    $0, %eax
        notl    %eax

finish:
        popl    %ebp
        ret
