        .data
inp:
        .string "%d %d %d %d"
ans:
        .string "%d\n"
        .text
        .global process
process:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $20, %esp
        movl    $0, -4(%ebp) 
        jmp     scan
right:
        movl    -12(%ebp), %eax 
        cmpl    %eax, -20(%ebp)
        jle     left
        movl    -12(%ebp), %eax 
        movl    %eax, -20(%ebp)
left:
        movl    -8(%ebp), %eax
        cmpl    %eax, -16(%ebp)
        jge     sum
        movl    -8(%ebp), %eax
        movl    %eax, -16(%ebp)
sum:
        movl    -20(%ebp), %eax
        subl    -16(%ebp), %eax
        cltd
        notl    %edx
        andl    %edx, %eax
        addl    %eax, -4(%ebp)
scan:
        leal    -20(%ebp), %eax
        pushl   %eax
        leal    -16(%ebp), %eax
        pushl   %eax
        leal    -12(%ebp), %eax
        pushl   %eax
        leal    -8(%ebp), %eax 
        pushl   %eax
        pushl   $inp
        call    scanf
        cmpl    $4, %eax
        je      right
        pushl   -4(%ebp)
        pushl   $ans
        call    printf
        movl    $0, %eax
        movl    %ebp, %esp
        popl    %ebp
        ret