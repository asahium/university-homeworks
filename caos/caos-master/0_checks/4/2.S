        .text
        .global process
process:
        push    %ebp
        mov     %esp, %ebp
        push    %esi
        push    %edi
        subl    $8, %esp

        movl    8(%ebp), %ecx
        movl    12(%ebp), %edi

        movl    (%ecx), %eax
        mull    8(%ecx, %edi, 4)

        movl    %edx, -16(%ebp)
        movl    %eax, -20(%ebp)

        movl    4(%ecx), %eax
        imull   24(%ecx)

        add     %eax, -20(%ebp)
        adc     %edx, -16(%ebp)

        jo      overflow
        movl    -16(%ebp), %edx
        movl    -20(%ebp), %eax
end:    
        addl    $8, %esp
        pop     %edi
        pop     %esi
        mov     %ebp, %esp
        pop     %ebp
        ret
overflow:
        movl    $0xffffffff, %eax
        movl    $0xffffffff, %edx
        jmp     end