        .text
        .global main
main:
        call    readi32
        mov     %eax, %ebx
        cmpl    $0, %eax
        jge     pr
        call    finish

pr:
        mov     %ebx, %eax
        call    writei32
        call    nl
        decl    %ebx
        cmpl    $0, %ebx
        jge     pr
        call    finish
