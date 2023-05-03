// Comment by Judge: Строка 54 - при работе функций для выделения места под временную переменную предпочтительнее использовать стек (иначе память под временную переменную Вы выделяете на всё время работы программы) - переделайте
// Comment by Judge: Если есть возможность для временной переменной использовать регистр, то стоит использовать именно его (регистр).



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
