#include <sys/syscall.h>
    .global writeu32
make_powers:
    push    %ebp
    mov     %esp, %ebp
    sub     $4, %esp
    movl    $1, %edx
    movl    $0, (%esp)
pow_loop:
    mov     %edx, (%eax)
    add     $4, %eax

    call    mult
    add     $1, (%esp)
    cmp     $10, (%esp)
    jne     pow_loop

    mov     %ebp, %esp
    pop     %ebp
    ret

mult:
    push    %ebp
    mov     %esp, %ebp
    sub     $8, %esp
    mov     %edx, 4(%esp)
    movl    $0, (%esp)
mult_loop:
    add     4(%esp), %edx
    add     $1, (%esp)
    cmp     $9, (%esp)
    jne     mult_loop

    mov     %ebp, %esp
    pop     %ebp
    ret

calc_digits:
    push    %ebp
    mov     %esp, %ebp
    sub     $4, %esp
    mov     %eax, %edx
    movl    $0, (%esp)
    sub     $4, %eax
calc_loop:
    movb    $'0', (%edx)
    jmp     cur_dig
continue:
    sub     $4, %eax
    add     $1, (%esp)
    inc     %edx
    cmp     $10, (%esp)
    jne     calc_loop

    mov     %ebp, %esp
    pop     %ebp
    ret

cur_dig:
    sub     (%eax), %ecx
    jc      overflow
    addb    $1, (%edx)
    jmp     cur_dig

overflow:
    add     (%eax), %ecx
    jmp     continue

write:
    push    %ebp
    mov     %esp, %ebp
    mov     $SYS_write, %eax
    mov     $STDOUT, %ebx
    mov     $1, %edx
    int     $0x80
    mov     %ebp, %esp
    pop     %ebp
    ret

writeu32:
    .equ    STDOUT, 1
    push    %ebp
    mov     %esp, %ebp
    push    %ebx
    sub     $50, %esp
    mov     %esp, %eax
    call    make_powers
    call    calc_digits
    mov     %esp, %ecx
    mov     %esp, %edx
    add     $50, %edx
    add     $40, %ecx
scip_zeros:
    cmp     %ecx, %edx
    je      zero_case
    cmpb    $'0', (%ecx)
    jne     next
    inc     %ecx
    jmp     scip_zeros

next:
    cmp     %ecx, %edx
    je      end
    push    %edx
    call    write
    pop     %edx
    inc     %ecx
    jmp     next

zero_case:
    mov     %esp, %ecx
    add     $40, %ecx
    call    write

end:
    add     $50, %esp
    pop     %ebx
    mov     %ebp, %esp
    pop     %ebp
    ret
