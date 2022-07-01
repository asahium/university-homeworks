        .text
        .global countrec
countrec:
        push    %ebp
        mov     %esp, %ebp
        push    %esi
        movl    $0, %edx
        movl    8(%ebp), %esi
        movl    (%esi), %eax
        movl    4(%esi), %ecx
        addl    %eax, %ecx
loop:
        cmpl    4(%ebp), %eax
        jg      add
        cmpl    4(%ebp), %ecx
        jle     add
        inc     %edx
add:
        movl    (%ebp), %ebp
        test    %ebp, %ebp
        jne     loop
        movl    8(%esi), %eax
        movl    %edx, (%eax)
        pop     %esi
        pop     %ebp
        ret