    .text
    .global main
main:
    xorl    %esi, %esi
    xorl    %edi, %edi
    jmp     read_dir

read_dir:
    call    readi32
    mov     %eax, %ebx
    jns     odd_check

    mov     %esi, %eax
    call    writei32
    mov     %edi, %eax
    call    writei32
    call    finish

odd_check:
    mov     %eax, %ebx
    andl    $1, %eax
    cmp     $0, %eax
    jnz     odd_case
    addl    %ebx, %esi
    jmp     read_dir

odd_case:
    addl    %ebx, %edi
    jmp     read_dir
