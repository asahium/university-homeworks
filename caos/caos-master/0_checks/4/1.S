        .text
        .global forward.args
forward.args:
        push    %ebp
        movl    %esp, %ebp
        subl    $8, %esp
        movl    12(%ebp), %eax
        movl    %eax, -4(%ebp)
        movl    16(%ebp), %eax
        cltd
        push    8(%ebp)
        push    %edx
        push    %eax
        push    20(%ebp)
        call    process
        addl    $16, %esp
        negl    %eax
        leave
        ret