### Условие

Напишите функцию std::string CommonSuffix(const std::string& a, const std::string& b), возвращающую наибольший общий суффикс двух данных строк.

(Суффиксом строки называется всякая подстрока этой строки, на которую исходная строка заканчивается. Например, суффиксы слова apple — пустая строка, e, le, ple, pple, apple. Для слов apple и tuple наибольшим общим суффиксом является ple.)
Примечания

В вашем решении должна быть только эта функция и необходимые для неё директивы #include. Мы сами протестируем её работу с помощью своей функции main. 

### Решение
```cpp
#include <iostream>
#include <string>

std::string CommonSuffix(const std::string& a, const std::string& b) {
    std::string suff, answer;
    int i1 = a.length();
    int i2 = b.length();
    int i_min;
    if (i1 > i2)
        i_min = i2;
    else
        i_min = i1;
    int i = 0;
    while (i < i_min && (a[i1 - 1 - i] == b[i2 - 1 - i])) {
        suff += a[i1 - 1 - i];
        ++i;
    }
    for (int i = suff.length() - 1; i >= 0; i--)
        answer += suff[i];
    return answer;
}
```
