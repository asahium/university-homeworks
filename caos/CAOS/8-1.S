        .data
str:    .asciz  "%d %d %d\n"
        .text
        .global print_fib

print_fib:
        pushl   %ebp
        movl    %esp, %ebp
        movl    A, %eax
        addl    B, %eax
        movl    %eax, %ecx
        addl    B, %ecx
        movl    %ecx, %edx
        addl    %eax, %edx
        pushl   %edx
        pushl   %ecx
        pushl   %eax
        pushl   $str
        call    printf
        movl    %ebp, %esp
        popl    %ebp
        ret