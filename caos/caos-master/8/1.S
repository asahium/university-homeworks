        .text
        .global main
main:
        call    readi32
        mov     %eax, %ebx
        call    readi32
        addl    %ebx, %eax
        call    writei32
        call    nl
        call    finish
