___
## Разбор задачи "Диагональ"

### Условие
Реализуйте функцию с заголовком
```cpp
bool CheckAntiDiagonalSymmetry(const std::vector<std::vector<int>>& matrix);
```
Функция принимает квадратную матрицу и возвращает `true`, если матрица является симметричной относительно побочной диагонали, и `false` иначе.

Гарантируется, что матрица является квадратной размера n × n, где 0 ≤ n ≤ 100.

Побочная диагональ матрицы - это диагональ, проходящая из левого нижнего угла в правый верхний (при условии, что индексы строк и столбцов нумеруются сверху вниз и слева направо).
В вашем решении должна быть только эта функция и необходимые директивы `#include`. Мы сами протестируем её работу с помощью своей функции `main`.

### Решение
Сначала надо понять, как для элемента с индексами `i, j` найти индексы симметричного элемента.
Это будут индексы `matrix.size() - 1 - j` и `matrix.size() - 1 - i`.
Вычитание единицы возникает из-за того, что индексы нумеруются с нуля.

Теперь самое простое решение - проверить для каждого элемента матрицы что он равен симметричному:
```cpp
#include <vector>

bool CheckAntiDiagonalSymmetry(const std::vector<std::vector<int>>& matrix) {
    for (size_t i = 0; i != matrix.size(); ++i) {
        for (size_t j = 0; j != matrix.size(); ++j) {
            if (matrix[i][j] != matrix[matrix.size() - 1 - j][matrix.size() - 1 - i]) {
                return false;
            }
        }
    }
    return true;
}
```

Конечно, можно уменьшить перебор в два раза: достаточно перебирать только элементы, лежащие выше побочной диагонали.
Напишите такой вариант сами.

Типичная ошибка здесь у многих - ограничиваться только элементами выше главной диагонали:
```cpp
    for (size_t i = 0; i != matrix.size(); ++i) {
        for (size_t j = 0; j != i; ++j) {  // ошибка!
            // ...
        }
    }
```
___
## Разбор задачи "Функция Join"

### Условие
Вам требуется написать функцию `Join` со следующим заголовком:
```cpp
std::string Join(const std::vector<std::string>& tokens, char delimiter);
```
Функция должна вернуть строку, полученную склейкой элементов вектора через указанный разделитель.
Например, `Join({"What", "is", "your", "name?"}, '_')` должна вернуть строку `"What_is_your_name?"`.

Сдайте в систему код функции с необходимыми директивами `#include`. Ваша функция будет протестирована с помощью нашей программы.

### Решение
Будем идти по вектору и добавлять в ответ разделитель и очередной токен. Важно, чтобы разделители не оказались по краям - они должны быть только между токенами.

Студенты часто спрашивают, может ли в функцию передаваться пустой или одноэлементный вектор? Конечно, может! В этом случае, очевидно, надо вернуть пустую строку или строку из одного элемента вектора, соответственно.

```cpp
#include <string>
#include <vector>

std::string Join(std::vector<std::string>& tokens, char delim) {
    std::string result;
    for (const auto& token : tokens) {
        if (!result.empty()) {  // добавляем разделитель только если что-то уже добавили раньше
            result += delim;
        }
        result += token;
    }
    return result;
}
```

Есть вариант решения, где разделитель добавляется в конце всегда, а потом - если строка оказалась непустой - удаляется из неё:
```cpp
#include <string>
#include <vector>

std::string Join(std::vector<std::string>& tokens, char delim) {
    std::string result;
    for (const auto& token : tokens) {
        result += token;
        result += delim;
    }
    if (!result.empty()) {
        result.pop_back();
    }
    return result;
}
```
Этот вариант плох тем, что может привести к лишней реаллокации строки `result` из-за последнего разделителя.
___
## Разбор задачи "Общий префикс строк"

### Условие
Напишите функцию `std::string CommonPrefix(const std::vector<std::string>& words)`,
вычисляющую наибольший общий префикс строк, переданных в векторе `words`.
Например, для пустого вектора нужно вернуть пустую строку, а для вектора из строк `apple`, `apricot` и `application` — строку `ap`.

В вашем решении должны быть только подключения необходимых библиотек и функция `CommonPrefix`.
В решении могут быть и ваши вспомогательные функции (если они вам нужны). Мы скомпилируем ваш код с нашей функцией `main`.

### Решение
Давайте напишем вспомогательную функцию, вычисляющую общий префикс двух строк.
Для этого будем идти по символам строк и проверять, равны ли они.
Важно не выйти за пределы строки.
```cpp
#include <string>
#include <vector>

std::string CommonPrefix(const std::string& a, const std::string& b) {
    size_t i = 0;
    while (i != a.size() && i != b.size() && a[i] == b[i]) {
        ++i;
    }
    return a.substr(0, i);
}
```

Теперь можно просто перебрать поданные на вход строки и вычислять на каждом шаге общий префикс у текущей строки и старого префикса:
```cpp
std::string CommonPrefix(const std::vector<std::string>& words) {
    if (words.empty()) {
        return {};
    }
    std::string prefix = words[0];
    for (size_t i = 1; i != words.size() && !prefix.empty(); ++i) {
        prefix = CommonPrefix(prefix, words[i]);
    }
    return prefix;
}
```
Здесь мы вызываем в цикле первую функцию `CommonPrefix`. Компилятор понимает какую из функций надо вызвать по типам аргументов (здесь передаётся не вектор строк, а две строки).

Недостаток этого решения в том, что мы много раз создаём новые строки (префиксы), хотя на самом деле все они являются подстроками первой строки.
Поэтому давайте перепишем первую функцию, чтобы она использовала `string_view`.
Во второй функции объявим `prefix` с явным типом `string_view`, а в конце вернём `std::string(prefix)`:
преобразование из `string_view` обратно в `string` надо описывать явно.
```cpp
#include <string>
#include <string_view>
#include <vector>

std::string_view CommonPrefix(const std::string_view a, const std::string_view b) {
    size_t i = 0;
    while (i != a.size() && i != b.size() && a[i] == b[i]) {
        ++i;
    }
    return a.substr(0, i);
}

std::string CommonPrefix(const std::vector<std::string>& words) {
    if (words.empty()) {
        return {};
    }
    std::string_view prefix = words[0];
    for (size_t i = 1; i != words.size() && !prefix.empty(); ++i) {
        prefix = CommonPrefix(prefix, words[i]);
    }
    return std::string(prefix);
}
```


### Решение с синхронным проходом
Рассмотрим альтернативное решение.
Будем одновременно идти по всем словам.
Для этого удобно сначала вычислить их минимальную длину, чтобы было проще проверять, когда пора остановиться.

```cpp
#include <algorithm>
#include <string>
#include <vector>

std::string CommonPrefix(const std::vector<std::string>& words) {
    if (words.empty()) {
        return {};
    }

    size_t min_len = words[0].size();
    for (const auto& word : words) {
        min_len = std::min(min_len, word.size());
    }

    for (size_t i = 0; i < min_len; ++i) {
        const char c = words[0][i];
        for (const auto& word : words) {
            if (word[i] != c) {
                return word.substr(0, i);
            }
        }
    }

    return words[0].substr(0, min_len);
}
```

По сравнению с попарным решением есть преимущество: время работы равно `O(|result| * num_words)`, в отличие от попарного `O(sum len of words)`
Но есть и недостаток: при очень большом количестве слов нам придется постоянно обращаться к разным участкам памяти, а это может затормозить работу.
___
## Разбор задачи "Шифр Цезаря"

### Условие
Шифр Цезаря — это вид шифра подстановки, в котором каждый символ в открытом тексте заменяется символом, находящимся на некотором постоянном числе позиций левее или правее него в алфавите.
Если в алфавите меньше букв, чем получившийся номер буквы, то отсчет ведется с начала алфавита.

Если мы будем зашифровывать слово `kenig` используя сдвиг размером 13, то получим `xravt`.

Ваша задача состоит в том, что бы расшифровать строку.
Вам дана зашифрованная строка, состоящая не более чем из 1000 строчных или заглавных букв латинского алфавита.
Далее записан размер сдвига `k`, с помощью которого было зашифровано сообщение (0<=k<=10^9).

Выведете исходную строку.

Примеры ввода и вывода:

`xravt 13` => `kenig`.

`furg 3` => `crod`.

`ZaQzJzCzAqZ 51` => `AbRaKaDaBrA`.

### Решение
Во-первых, заметим, что в латинском алфавите 26 букв.
Далее, вместо сдвига `k` можно рассматривать его остаток от деления на 26 (так как если `k` >= 26, то всё равно всё будет сдвигаться по циклу).
Из второго примера следует, что `k` обозначает сдвиг вправо. Поэтому для расшифровки нам надо будет сдвигать буквы влево.

Отдельно надо разобраться со строчными и заглавными буквами: при сдвиге строчных должны получаться строчные, а при сдвиге заглавных - заглавные.
Нам достаточно знать, что в таблице ASCII и строчные и заглавные буквы идут подряд по алфавиту.
```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
    const int alphabet_size = 26;

    string word;
    cin >> word;

    unsigned int shift;
    cin >> shift;
    shift %= alphabet_size;

    for (size_t i = 0; i != word.size(); ++i) {
        bool upper = isupper(word[i]);
        word[i] = word[i] - shift;
        if (upper) {
            if (word[i] < 'A') {
                word[i] += alphabet_size;
            }
        } else {
            if (word[i] < 'a') {
                word[i] += alphabet_size;
            }
        }
    }

    cout << word << "\n";
}
```
Вместо вложенных `if` можно было бы использовать формулу для индексов с остатками от деления на `alphabet_size`.
___
## Разбор задачи "Утилита paste"

### Условие
Вам необходимо реализовать упрощенный аналог консольной утилиты paste.
В Linux эта утилита принимает на вход несколько файлов и выписывает очередные строки этих файлов, склеенные через знак табуляции.
В этой задаче отдельных входных файлов не будет: вместо этого данные будут просто последовательно подаваться на вход программы.

В первой строке указано неотрицательное целое `m` — количество "файлов".
Далее идёт `m` блоков данных.
В начале каждого блока сначала указано неотрицательное целое число `n_i` — количество строк очередного "файла".
Затем идут сами строки, состоящие из латинских букв, цифр и знаков пунктуации, но не содержащие пробельных разделителей (то есть, вы можете их читать просто через `std::cin >> word`).
Гарантируется, что строки непусты. Количество файлов, количество строк в каждом файле и количество символов в каждой строке не превосходит 100.

Выведите сначала первые строки всех файлов (склеив их через табуляцию), затем вторые строки и т. д.
В конце каждой строки должен быть напечатан символ перевода строки.
Если в каком-то из файлов строки закончатся раньше, не выводите в соответствующем поле ничего (но символ табуляции перед таким полем, если оно не первое, всё равно должен быть).

### Решение
Для тех, кто не знает, что такое символ табуляции: читайте [статью в Википедии](https://ru.wikipedia.org/wiki/Табуляция). Важно понимать, что табуляция не тождественна нескольким пробелам.

В задаче важно печатать табуляцию только между полями. Частая ошибка - печать табуляции в конце каждой строки. Визуально это неотличимо от примера вывода, но если выделить текст (или посмотреть на его байты в каком-нибудь редакторе), то табуляцию можно увидеть.

Считаем сначала все строки файлов в вектор векторов строк.
Затем аккуратно пройдёмся по элементам этого вектора и склеим строки:
```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main() {
    size_t files_count;
    std::cin >> files_count;
    std::vector<std::vector<std::string>> files(files_count);

    size_t max_lines_count = 0;
    for (size_t i = 0; i != files.size(); ++i) {
        size_t lines_count;
        std::cin >> lines_count;
        max_lines_count = std::max(max_lines_count, lines_count);
        files[i].resize(lines_count);
        for (size_t j = 0; j != lines_count; ++j) {
            std::cin >> files[i][j];
        }
    }

    for (size_t j = 0; j != lines_count; ++j) {
        for (size_t i = 0; i != files.size(); ++i) {
            if (i > 0) {
                std::cout << '\t';
            }
            if (j < files[i].size()) {
                std::cout << files[i][j];
            }
        }
        std::cout << '\n';
    }
}
```
Здесь мы используем индекс `i` для номера файла, а индекс `j` - для номера строки в файле.
Фактически нам надо "транспонировать" двумерный вектор, поэтому при выводе порядок циклов меняется местами.