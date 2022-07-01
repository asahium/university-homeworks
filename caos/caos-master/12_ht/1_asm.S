        .weak   __init_mem, __init_stdin, __init_stdout
        .weak   __fini_stdout, __fini_stdin, __fini_mem
        .global _start, _exit, exit
        .text
_start:
        pushl   %eax

        mov     $__init_mem, %eax
        cmpl    $0, %eax
        je      _istdin

        call    __init_mem
_istdin:
        mov     $__init_stdin, %eax
        cmpl    $0, %eax
        je      _istdout

        call    __init_stdin
_istdout:
        mov     $__init_stdout, %eax
        cmpl    $0, %eax
        je      _cmain

        call    __init_stdout
_cmain:
        popl    %eax
        popl    %eax
        leal    (%esp,%eax,4), %ecx
        addl    $4, %ecx
        movl    %esp, %ebx
        pushl   %ecx
        pushl   %ebx
        pushl   %eax

        call    main
        pushl   %eax
        call    exit
exit:
        pushl   %ebp
        movl    %esp, %ebp

        mov     $__fini_stdout, %eax
        cmpl    $0, %eax
        je      _fstdin

        call    __fini_stdout
_fstdin:
        mov     $__fini_stdin, %eax
        cmpl    $0, %eax
        je      _fmem

        call    __fini_stdin
_fmem:
        mov     $__fini_mem, %eax
        cmpl    $0, %eax
        je      _argexit

        call    __fini_mem
_argexit:
        pushl   8(%ebp)
        call    _exit
_exit:
        pushl   %ebp
        movl    %esp, %ebp

        movl    $1, %eax
        movl    8(%ebp), %ebx
        int     $0x80

