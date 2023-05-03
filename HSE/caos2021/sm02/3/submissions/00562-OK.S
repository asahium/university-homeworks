    .global process
process:
    push    %ebp
    mov     %esp, %ebp
loop:
    call    readi32
    jc      print

    push    %eax
    jmp     loop
print:
    cmp     %esp, %ebp
    je      exit

    pop     %eax
    call    writei32
    jmp     print
exit:
    mov     %ebp, %esp
    pop     %ebp
    ret
