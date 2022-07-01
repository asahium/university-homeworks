.text  
format:
        .asciz "%llu\n"
.global process

process:
        push    %ebp
        mov     %esp, %ebp
        push    %esi
        push    %edi
        
        movl    A, %eax
        movl    A+4, %edx
        sal     %eax
        rcl     $1, %edx
        movl    B, %esi
        movl    B+4, %edi
        shr     %edi
        rcr     $1, %esi
        sub     %esi, %eax
        sbbl    %edi, %edx
        
        push    %edx
        push    %eax
        push    $format
        call    printf
        
        lea     -8(%ebp), %esp
        pop     %edi
        pop     %esi
        pop     %ebp
        ret