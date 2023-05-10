|                      |       |
|----------------------|-------|
| **Time limit:**      | `3 s` |
| **Real time limit:** | `4 s` |
| **Memory limit:**    | `64M` |


### Problem ku08-3: kr08-3 (дореш)

Напишите программу `./blockwise_hash seed msg_len block_size`, которая генерирует msg_len байт
случайных данных, и каждые block_size байт хеширует. seed, msg_len, block_size - целые числа,
записанные в десятичном виде. Для генерации случайных данных используйте функцию `(char)rand()`
стандартной библиотеки Си с приведением к типу char. Для задания seed генератора псевдослучайных
чисел используйте функцию `srand(seed)` стандартной библиотеки Си с предоставленным значением seed.
Обратите внимание, что данные должны генерироваться последовательно.

Для хеширования данных используйте функцию `void some_hash(char* data, size_t n, char* out) `, где
data - массив данных, от которых вы хотите взять хеш, n - размер этого массива, out - указатель на
массив выходных данных. Функция some_hash предоставляется извне. Количество памяти, необходимое
указателю char* out, вы должны получить из функции `size_t get_hash_size()` Гарантируется, что char*
out после вызова функции some_hash - null-terminated строка.

Программа должна для каждого отдельного блока вывести строку `[block_no]\thash(block)\n`, где
block_number - номер блока, hash - значение хэш-функции от этого блока. Нумерация блоков начинается
с единицы.

Обратите внимание, что msg_len может быть слишком большим для того, чтобы хранить его в памяти
полностью.

Обратите внимание, что порядок вывода хешей должен совпадать с порядком блоков данных. Т.е. нельзя
вывести сначала хеш от блока с номером 2, а потом хеш от блока с номером 1.

Обратите внимание, что последний блок в сообщении может быть меньше, чем block_size (т.е. msg_len не
кратен block_size). В таком случае нужно взять хеш только от реального размера блока.

Гарантируется, что памяти процесса достаточно для выделения 4 * block_size байт (и даже немного
больше). Гарантируется, что дополнительных 4 потоков достаточно для решения задачи.

### Examples

#### Input

    
    
    ./blockwise_hash 42 4100 2048

#### Output

    
    
    [1]\tthis_block_is_good
    [2]\tthis_block_is_bad
    [3]\tthis_block_is_ugly
    
