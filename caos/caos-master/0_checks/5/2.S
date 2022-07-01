        .text
        .global process
process:
        pushl   %edi
        movl    $3, %edx
        movl    8(%esp), %eax
        movl    12(%esp), %ecx
        movl    (%eax), %edi
        subl    %ecx, %edx
        movsd   (%edi,%ecx,8), %xmm0
        subsd   4(%eax,%edx,8), %xmm0
        mulsd   %xmm0, %xmm0
        movsd   %xmm0, 36(%eax)
        popl    %edi
        ret