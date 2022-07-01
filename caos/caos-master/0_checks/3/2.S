        .text
        .global process
process:
        pushl   %ebp
        movl    %esp, %ebp
        
        subl    $20, %esp
        movl    12(%ebp), %eax
        movb    %al, -20(%ebp)
        
        movl    $0, %edx
        movl    $5, %eax
        
        imull   16(%ebp), %eax
        
        jno     .L2
        movl    $1, %edx
.L2:
        movl    %eax, -4(%ebp)
        movl    %edx, %eax
        andl    $1, %eax
        testb   %al, %al
        je      .L4
        movl    $1, %eax
        jmp     fin
.L4:
        movsbl  -20(%ebp), %eax

        movl    $0, %edx
        sall    $2, %eax

        movl    %eax, -8(%ebp)
        movl    %edx, %eax

        andl    $1, %eax
        testb   %al, %al

        je      .L6
        movl    $1, %eax
        jmp     fin
.L6:
        movsbl  -20(%ebp), %eax
        movl    $0, %ecx
        movl    16(%ebp), %edx
        subl    %eax, %edx
        movl    %edx, %eax
        jno     .L7
        movl    $1, %ecx
.L7:
        movl    %eax, -12(%ebp)
        movl    %ecx, %eax
        andl    $1, %eax
        testb   %al, %al
        je      write
        movl    $1, %eax
        jmp     fin
write:
        movl    -12(%ebp), %edx
        movl    8(%ebp), %eax
        movl    %edx, (%eax)
        movl    $0, %eax
fin:
        leave
        ret