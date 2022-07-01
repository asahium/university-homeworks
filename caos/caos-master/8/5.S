        .text
        .global main
main:
        xorl    %edi, %edi
        xorl    %esi, %esi
        jmp     read_dir

read_dir:
        call    readi32
        mov     %eax, %ebx
        jns     oddchk

        mov     %esi, %eax
        call    writei32
        call    nl
        mov     %edi, %eax
        call    writei32
        call    nl
        call    finish

oddchk:
        mov     %eax, %ebx
        andl    $1, %eax
        cmp     $0, %eax
        jnz     odd
        addl    %ebx, %esi
        jmp     read_dir

odd:
        addl    %ebx, %edi
        jmp     read_dir
