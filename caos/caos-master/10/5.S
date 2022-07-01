        .text
f64:    .string  "%llx\n"
f128:   .string  "%llx%016llx\n"
        .global mul64p
mul64p:
        push    %ebp
        movl    %esp, %ebp

        subl    $16, %esp

        movl    16(%ebp), %ecx
        movl    8(%ebp), %eax

        mull    %ecx

        movl    %edx, -4(%ebp)
        movl    %eax, -8(%ebp)
        movl    12(%ebp), %eax

        mull    %ecx

        movl    %edx, (%esp)

        addl    %eax, -4(%ebp)
        adcl    $0, (%esp)

        movl    20(%ebp), %ecx

        movl    8(%ebp), %eax
        movl    $0, 4(%esp)

        mull    %ecx

        addl    %eax, 12(%esp)

        adcl    %edx, (%esp)
        adcl    $0, 4(%esp)

        movl    12(%ebp), %eax

        mull    %ecx

        addl    %edx, 4(%esp)
        addl    %eax, (%esp)

        adcl    $0, 4(%esp)

        movl    (%esp), %eax

        orl     4(%esp), %eax

        cmpl    $0, %eax
        jne     p128

        addl    $8, %esp

        push    $f64
        call    printf

        jmp     end
p128:
        push    $f128
        call    printf
end:
        leave
        ret