    .text
    .global main
main:
    mov    $1, %edx
loopread:
    call   readi32	
    jc     result
    cmp    $0, %eax
    js     down
up:
    mov    %eax, %ecx
    call   readi32
    test   %ecx, %ecx
    jnz    not_zero
    mov    %eax, array(, %edx, 8)
    mov    $array, %eax
    mov    %eax, array+4(, %edx, 8)
    inc    %edx
    jmp    loopread
not_zero:
    shl    $3, %ecx
    add    $array, %ecx
    mov    %ecx, array+4(, %edx, 8)
    mov    %eax, array(, %edx, 8)
    inc    %edx
    jmp    loopread
down:
    mov    %eax, %ecx
    sar    $31, %ecx
    xor    %ecx, %eax
    sub    %ecx, %eax
    mov    array+4(, %eax, 8), %ecx
    cmp    $0, %ecx
    jne    not_empty
    mov    $-1, %eax
    call   writei32
    jmp    loopread
not_empty:
    mov    array(, %eax, 8), %eax
    call   writei32
    mov    (%ecx), %eax
    mov    %eax, array(, %edx, 8)
    mov    4(%ecx), %eax
    mov    %eax, array+4(, %edx, 8)
    inc    %edx
    jmp    loopread
result:
    call   finish

    .data
array:
    .skip  8008
