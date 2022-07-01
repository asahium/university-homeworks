        .text
        .global forward.args
forward.args:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $24, %esp
        movl    8(%ebp), %eax
        movl    %eax, -16(%ebp)
        movl    20(%ebp), %ecx
        subl    $4, %esp
        pushl   -16(%ebp)
        pushl   $0
        pushl   16(%ebp)
        call    process
        addl    $16, %esp
        movl    $0, %edx
        leave
        ret