|                      |       |
|----------------------|-------|
| **Time limit:**      | `1 s` |
| **Real time limit:** | `5 s` |
| **Memory limit:**    | `64M` |


### Problem ku06-1: kr06-1 (дореш)

Дан тип указателя на функцию: `typedef int (*func_t)(void*)`.

Напишите на языке ассемблера x86 функцию, соответствующую прототипу:

    
    
    int run_on_stack(func_t func, void* arg, void* stack_bottom);

Пользователь `run_on_stack` аллоцирует блок памяти `char* M` некоторого неизвестного нам размера
`size`, который планирует использовать как стек для функции func, и передаёт в `run_on_stack` адрес
первого свободного байта после `M` (указатель `M + size`).

`run_on_stack` должна запустить функцию func с аргументом arg на переданном ей стеке (то есть таким
образом, чтобы локальные переменные функции func хранились внутри блока памяти `M`) и вернуть то
значение, которое вернёт func.

Например, должен работать такой код:

    
    
    int i_love_large_stacks(void* arg) {
        int local_array[4 << 20]; // 16-megabyte array
        local_array[0] = 42;
        ...
        return 3;
    }
    
    const size_t stacksize = 50 << 20; // 50 MB
    char* stack = malloc(stacksize);
    int result = run_on_stack(i_love_large_stacks, NULL, stack + stacksize);
    assert(result == 3);

