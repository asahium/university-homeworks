pushl   %edi
        pushl   %esi
        movl    16(%esp), %eax
        movl    12(%esp), %edi
        movl    8(%edi,%eax,4), %eax
mull    (%edi)
movl    %eax, %ecx
        movl    24(%edi), %eax
        movl    %edx, %esi
        imull   4(%edi)
addl    %ecx, %eax
        adcl    %esi, %edx
        popl    %esi
        popl    %edi
        retl