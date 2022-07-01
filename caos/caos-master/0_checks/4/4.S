        .text
        .global addbe
addbe:
        push    %ebp
        mov     %esp, %ebp
        push    %ebx
        push    %esi
        push    %edi

        movl    8(%ebp), %ebx
        movl    $0, %esi
loop:
        decl    %ebx

        movl    12(%ebp), %ecx

        movl    $0, %eax
        movl    $0, %edx

        movb    (%ecx, %ebx, 1), %eax

        movl    16(%ebp), %ecx
        movb    (%ecx, %ebx, 1), %edx

        addl    %edx, %eax
        addl    %esi, %eax
        movl    $0, %esi

        cmpl    $0xff, %eax
        jbe     put

        movl    $1, %esi

put:
        movl    20(%ebp), %ecx
        movb    %eax, (%ecx, %ebx, 1)

        test    %ebx, %ebx
        jne     loop

        test    %esi, %esi
        jnz     err
        movl    $0, %eax
end:
        pop     %edi
        pop     %esi
        pop     %ebx
        mov     %ebp, %esp
        pop     %ebp
        ret
err:
        movl    $1, %eax
        jmp     end
