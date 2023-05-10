|                      |       |
|----------------------|-------|
| **Time limit:**      | `1 s` |
| **Real time limit:** | `5 s` |
| **Memory limit:**    | `64M` |


### Problem sm09-2: c/inline-asm/hello-nostdlib

Напишите программу, которая печатает на стандартный поток вывода строку "hello world" (без кавычек)
и перевод строки, а затем успешно завершается.

Ваша программа будет компилироваться с опцией `-nostdlib` и не сможет воспользоваться функциями из
стандартной библиотеки языка Си. Точка входа в программу — функция `_start`.

Заготовка для программы:

    
    
    #include <sys/syscall.h>
    
    void _start() {
        // обратиться к системному вызову write
        // обратиться к системному вызову exit
    }

Обратите внимание, что оптимизатор может удалить из программы ассемблерную вставку, output-ы которой
никак не используются. Чтобы этого не произошло, необходимо пометить вставку как имеющую побочные
эффекты c помощью ключевого слова `volatile`:

    
    
    asm volatile ( "int $0x80" : ... ); // do not remove this asm block
