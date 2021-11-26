    .text
    .global partition
partition:
    push    %ebp
    mov     %esp, %ebp

continue:
    mov     %ebx, %ecx
    mov     %ebx, %edx
    add     %esi, %edx
    add     %esi, %edx
    sub     $2, %edx

loop:
    cmp     %ecx, %edx
    je      result

    jmp     try

try:
    movswl  (%ecx), %eax
    cmp     %edi, %eax
    js      first

    movswl  (%edx), %eax
    cmp     %edi, %eax
    jns     second

    mov     (%ecx), %ax
    mov     %ax, temp
    mov     (%edx), %ax
    mov     %ax, (%ecx)
    mov     temp, %ax
    mov     %ax, (%edx)
    jmp     loop

first:
    add     $2, %ecx
    jmp     loop

second:
    sub     $2, %edx
    jmp     loop		

result:
    sub     %ebx, %edx
    shr     $1, %edx

    mov     %ebp, %esp
    pop     %ebp
    ret

    .data
temp:
    .skip 2
