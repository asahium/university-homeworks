        .data
ss: 
        .string "%d"
ps:   
        .string "%d "
nl:
        .string "\n"
        .text
        .global process
process:
        push    %ebp
        movl    %esp, %ebp

        pushl   %esi

        subl    $8, %esp

        leal    -4(%ebp), %eax
        movl    $0, -8(%ebp)

        push    %eax
        push    $ss
        call    scanf

        addl    $8, %esp

        cmpl    $0, -4(%ebp)
        je      end
read:
        subl    $4, %esp
        leal    (%esp), %eax

        push    %eax
        push    $ss
        call    scanf

        addl    $8, %esp

        incl    -8(%ebp)
        movl    -8(%ebp), %eax

        cmpl    %eax, -4(%ebp)
        jne     read

        movl    $0, -8(%ebp)
write:
        push    $ps
        call    printf

        addl    $8, %esp

        incl    -8(%ebp)
        movl    -8(%ebp), %eax

        cmpl    %eax, -4(%ebp)
        jne     write
end:
        push    $nl
        call    printf

        leave
        ret