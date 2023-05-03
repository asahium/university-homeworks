.text
    .global main
main:
    sub $4, %esp
    push %ebp
    mov %esp, %ebp
    add $8, %esp
    call process
next:
    call writei32
    call finish
