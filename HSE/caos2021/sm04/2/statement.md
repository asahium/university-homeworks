|                      |       |
|----------------------|-------|
| **Time limit:**      | `1 s` |
| **Real time limit:** | `5 s` |
| **Memory limit:**    | `64M` |


### Problem sm04-2: asm/mem/free

Напишите подпрограмму `free_mem`, которая «освобождает» память, выделенную на куче (то есть помещает
блок памяти в список свободных).

Подпрограмма `free_mem` принимает один параметр — адрес, который ранее вернула подпрограмма
`alloc_mem` (см. предыдущую задачу). Соответствующий блок памяти должен быть добавлен в голову
списка `freelist`, который должен быть определён в сдаваемом файле. Структуру списка `freelist`
также см. в предыдущей задаче.

Подпрограмма `free_mem` не возвращает никакого результата. Соблюдайте стандартные соглашения о
вызове (cdecl).
