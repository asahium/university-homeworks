.global process
.text

process:
        pushl    %ebp
        movl     %esp, %ebp
        movl     8(%ebp), %eax
        movl     12(%ebp), %ecx
        movl     16(%ebp), %edx
        movl     (%eax, %ecx, 4), %ecx
        addl     64(%eax, %edx, 4), %ecx
        sar      $1, %ecx
        movl     %ecx, %eax
        movl     %ebp, %esp
        pop      %ebp
        ret