    .global main
main:
    mov    $0, %eax
    mov    $0, %ebx
    mov    $0, %ecx

read_dir:
    mov    %eax, %ecx
    add    %eax, %ebx
    jo     overflow
    call   readi32
    jnc    read_dir
    mov    %ebx, %eax
    call   writei32
    call   finish

overflow:
    mov    $2147483647, %eax
    mov    $-2147483648, %edx
    cmp    %ecx, %ebx
    cmovg  %edx, %eax
    call    writei32
    call    finish
