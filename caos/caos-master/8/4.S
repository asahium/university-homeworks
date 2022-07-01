        .text
        .global main
main:
        movl    $0, %ebx
        movl    $0, %ecx
read_dir:
        call    readi32
        jc      fin
        addl    %eax, %ebx
        jno     read_dir
        adcl    $0, %ecx
        movl    $0x7ffffffe, %ebx
        addl    %ecx, %ebx
fin:
        movl    %ebx, %eax
        call    writei32
        call    nl
        call    finish
