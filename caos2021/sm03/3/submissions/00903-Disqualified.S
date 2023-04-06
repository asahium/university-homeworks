#include <sys/syscall.h>
    .global strtou256
add:
    push    %ebp
    mov     %esp, %ebp
    push    %eax
    push    %ecx
    push    %edx
    call    u256mul10reg
    pop     %edx
    mov     %esi, %eax
    xor     %ecx, %ecx
    subb    $'0', %dl
    addb    %dl, (%eax)
    jnc     end_add
add_loop:
    inc     %eax
    inc     %ecx
    cmp     $32, %ecx 
    je      end_add
    addb    $1, (%eax)
    jc      add_loop
end_add:
    pop     %ecx
    pop     %eax
    mov     %ebp, %esp
    pop     %ebp
    ret

strtou256:
    push    %ebp
    mov     %esp, %ebp
    push    %esi
    mov     16(%ebp), %esi
    mov     8(%ebp), %eax
    xor     %ecx, %ecx

zero:
    movl    $0, (%esi, %ecx, 4)
    inc     %ecx
    cmp     $8, %ecx
    jne     zero

    xor     %ecx, %ecx

move_loop:
    movb    (%eax, %ecx, 1), %dl
    cmp     $'0', %dl
    jl      continue
    cmp     $'9', %dl
    jg      continue
    call    add

    inc     %ecx
    cmp     12(%ebp), %ecx
    je      continue
    jmp     move_loop

continue:
    mov     %ecx, %eax

    pop     %esi
    mov     %ebp, %esp
    pop     %ebp
    ret
