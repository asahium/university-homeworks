    .globl main
main:
    call    readi64
    shl     $1, %edx
    shl     $1, %eax
    adc     $0, %edx
    mov     %eax, %ecx
    mov     %edx, %ebx

    call    readi64
    shr     $1, %eax
    mov     %edx, %esi
    and     $1, %esi
    shl     $31, %esi
    add     %esi, %eax
    shr     $1, %edx
    sub     %eax, %ecx
    sbb     %edx, %ebx
    mov     %ecx, %eax
    mov     %ebx, %edx

    call    writei64
    call    finish
