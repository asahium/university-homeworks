        .text
        .global mystrcmp
mystrcmp:
        pushl   %ebp
        movl    %esp, %ebp
        pushl   %esi
        pushl   %edi
        pushl   %ebx
        movl    8(%ebp), %esi
        movl    12(%ebp), %edi
cycle:
        movl    %esi, %eax
        movzbl  (%eax), %eax
        testb   %al, %al
        jz      eo
        movl    %edi, %ebx
        movzbl  (%ebx), %ebx
        testb   %bl, %bl
        jz      eo
        cmpb    %bl, %al
        ja      greater
        jb      lower
        incl    %esi
        incl    %edi
        jmp     cycle
eo:
        movl    %esi, %eax
        movzbl  (%eax), %eax
        testb   %al, %al
        jne     greater
        movl    %edi, %eax
        movzbl  (%eax), %eax
        testb   %al, %al
        jne     lower
        movl    $0, %eax
        jmp     fin
lower:
        movl    $-1, %eax
        jmp     fin
greater:
        movl    $1, %eax
fin:
        popl    %ebx
        popl    %edi
        popl    %esi
        popl    %ebp
        ret
