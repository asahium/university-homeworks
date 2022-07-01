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
        jz      eow
        movl    %edi, %ebx
        movzbl  (%ebx), %ebx
        testb   %bl, %bl
        jz      eow
        cmpb    %bl, %al
        ja      greater
        jb      lower
        incl    %esi
        incl    %edi
        jmp     cycle
eow:
        movl    %esi, %eax
        movzbl  (%eax), %eax
        testb   %al, %al
        jne     greater
        movl    %edi, %eax
        movzbl  (%eax), %eax
        testb   %al, %al
        jne     lower
        movl    $0, %eax
        jmp     finish
lower:
        movl    $-1, %eax
        jmp     finish
greater:
        movl    $1, %eax
finish:
        popl    %ebx
        popl    %edi
        popl    %esi
        popl    %ebp
        ret