        .text
        .global writeu32
writeu32:
        push    %ebp
        movl    %esp, %ebp
        push    %ebx
        push    %esi
        push    %edi
        movl    $9, %ebx
        xorl    %edi, %edi
        cmpl    $0, %ecx
        jne     .loop

        movl    $0, %ebx //
        movl    $0, %edx

        jmp     print
loop:
        cmpl    $0, %ebx
        jl      fin

        movl    $1, %eax
        movl    $10, %edx

        movl    %ebx, %esi
decimal_mask:
        cmpl    $0, %esi
        je      get_digit

        mull    %edx
        movl    $10, %edx
        decl    %esi
        jmp     decimal_mask
get_digit:
        movl    $0, %edx
get_digit_loop:
        cmpl    %eax, %ecx
        jb      end_loop
        incl    %edx
        subl    %eax, %ecx
        cmpl    $0, %edi
        jne     get_digit_loop
        movl    $1, %edi
        jmp     get_digit_loop
end_loop:
        decl    %ebx
        cmpl    $0, %edi
        jne     print
        jmp     loop
print:
        addl    $0, %edx

        push    %edx
        push    %ecx

        movl    stout, %edx
        movl    4(%esp), %ecx
        call    writechar

        popl    %ecx
        popl    %edx
        jmp     loop
fin:
        popl    %edi
        popl    %esi
        popl    %ebx
        movl    %ebp, %esp
        popl    %ebp
        ret