        .data
scn:
        .string "%d %d %d %d"
pri:
        .string "%d\n"
        .text
        .global process
process:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $20, %esp

        movl    $0, -4(%ebp) // res

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

        jge     add

        movl    -8(%ebp), %eax
        movl    %eax, -16(%ebp)
add:
        movl    -20(%ebp), %eax
        subl    -16(%ebp), %eax

        cltd

        notl    %edx

        andl    %edx, %eax
        addl    %eax, -4(%ebp)
scan:
        leal    -20(%ebp), %eax //-20, d
        pushl   %eax
        leal    -16(%ebp), %eax //-16, c
        pushl   %eax
        leal    -12(%ebp), %eax //-12, b
        pushl   %eax
        leal    -8(%ebp), %eax //-8, a
        pushl   %eax

        pushl   $scn

        call    scanf

        cmpl    $4, %eax
        je      right

        pushl   -4(%ebp)
        pushl   $pri

        call    printf

        movl    $0, %eax
        movl    %ebp, %esp
        popl    %ebp
        ret