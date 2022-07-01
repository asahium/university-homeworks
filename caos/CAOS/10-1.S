.text
.global process
process:
        subl    $4, %esp
cycle:
        movl    $3, %eax
        movl    $0, %ebx
        leal    (%esp), %ecx
        movl    $1, %edx
        int     $0x80
        cmpl    $0, %eax
        je      finish
        cmpl    $'0', (%esp)
        jl      rewrite
        cmpl    $'9', (%esp)
        jg      rewrite
        movl    $'0', (%esp)
rewrite:
        movl    $4, %eax
        movl    $1, %ebx
        leal    (%esp), %ecx
        movl    $1, %edx
        int     $0x80
        jmp     cycle
finish:
        movl    $1, %eax
        movl    $0, %ebx
        int     $0x80