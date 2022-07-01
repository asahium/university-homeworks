        .text
        .global minmax
minmax:
        push    %ebp
        mov     %esp, %ebp
        push    %edi
        push    %esi

        mov     (%eax), %esi
        mov     (%eax), %edi
loop:
        cmpl    (%eax), %edi
        cmovl   (%eax), %edi
        cmpl    (%eax), %esi
        cmovg   (%eax), %esi

        addl    $4, %eax
        decl    %edx
        cmpl    $0, %edx
        jne     loop
        mov     %esi, %eax
        mov     %edi, %edx
        pop     %esi
        pop     %edi
        leave
        ret