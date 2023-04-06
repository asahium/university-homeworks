### Условие

Вам требуется написать на C++ функцию со следующим заголовком:

std::vector<std::string> Split(const std::string& str, char delimiter);

Функция должна вернуть вектор строк, полученный разбиением строки str на части по указанному символу-разделителю delimiter. Если разделитель встретился в начале или в конце строки, то в начале (соответственно, в конце) вектора с результатом должна быть пустая строка. Если два разделителя встретились рядом, то пустая строка между ними тоже должна попасть в ответ. Для пустой строки надо вернуть пустой вектор.

### Решение
```cpp
#include <vector>

std::vector<std::string> Split(const std::string& str, char delimiter) {
    std::vector<std::string> answer;
    answer.clear();
    std::string slovo ="";
    long unsigned int i = 0;
    while (i < str.length()) {
        if (str[i] == delimiter) {
            answer.push_back(slovo);
            slovo = "";
        } else {
            slovo += str[i];
        }
        ++i;
    }
    answer.push_back(slovo);
    return answer;
}
```
