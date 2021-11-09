    .global main
main:
    mov $0, %edi
    mov $0, %esi
label:
    call readi32
    jc exit
    test $1, %eax
    jz odd
    add %eax, %esi
    jmp label
odd:
    add %eax, %edi
    jmp label
exit:
    mov %edi, %eax
    call writei32
    mov %esi, %eax
    call writei32
    call finish
