|                      |       |
|----------------------|-------|
| **Time limit:**      | `1 s` |
| **Real time limit:** | `5 s` |
| **Memory limit:**    | `64M` |


### Problem ku02-3: kr02-3 (дореш)

Дана структура:

    
    
    struct data {
        int (*get_rank)(const struct data*);
        char secret[];
    }

В массиве `struct data* elements[size]` лежат указатели на структуры data, причём
`elements[i]->get_rank(elements[i])` возвращает «ранг» соответствующего элемента.

Напишите функцию `void rank_sort(struct data* elements[], size_t size)`, которая сортирует указатели
в elements по возрастанию ранга элементов, на которые они указывают. Можно пользоваться стандартной
функцией `qsort(3)`.

В каждом тесте ранги всех элементов различны.

