.global stack_add

stack_add:
    pop %eax
    movl %eax, save
    pop %eax
    pop %edx
    add %edx, %eax
    push %eax
    movl (save), %eax
    push %eax
    ret

.data
save:
    .int 0
