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
    mov    $0x7fffffff, %eax
    mov    $0x80000000, %edx
    cmp    %ecx, %ebx
    cmovg  %edx, %eax
    call    writei32
    call    finish
