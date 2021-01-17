___
# A
Шахматный ферзь ходит по диагонали, горизонтали или вертикали. Даны две различные клетки шахматной доски. Определите, может ли ферзь попасть с первой клетки на вторую одним ходом.

**Формат ввода**

Программа получает на вход четыре числа от 1 до 8 каждое, задающие номер столбца и номер строки сначала для первой клетки, потом для второй клетки.

**Формат вывода**

Программа должна вывести YES, если из первой клетки ходом ферзя можно попасть во вторую, или NO в противном случае.

```c++
#include <iostream>

int main() {
    int x1, y1, x2, y2;
    std::cin >> x1 >> y1 >> x2 >> y2;
    if (abs(x2 - x1) == abs(y2 - y1) || x1 == x2 || y1 == y2) {
        std::cout << "YES\n";
    } else {
        std::cout << "NO\n";
    }
    return 0;
}
```

___
# B
По номеру дня недели (нумерация с единицы) выведите его сокращенное название. Названия должны быть такими:
mon
tue
wed
thu
fri
sat
sun

**Формат ввода**

Число от 1 до 7.

**Формат вывода**

Название дня недели из трех маленьких латинских букв.

```c++
#include <iostream>

int main() {
    int day;
    std::cin >> day;
    if (day == 1) {
        std::cout << "mon\n";
    } else if (day == 2) {
        std::cout << "tue\n";
    } else if (day == 3) {
        std::cout << "wed\n";
    } else if (day == 4) {
        std::cout << "thu\n";
    } else if (day == 5) {
        std::cout << "fri\n";
    } else if (day == 6) {
        std::cout << "sat\n";
    } else if (day == 7) {
        std::cout << "sun\n";
    }
    return 0;
}

```

___
# C
Вам требуется вычислить сумму цифр целого неотрицательного числа.

**Формат ввода**

Единственная строка входного файла содержит ровно одно целое число n, 0 ≤ n ≤ 109.

**Формат вывода**

Выведите сумму цифр этого числа.

```c++
#include <iostream>

int main() {
    int n;
    int sum = 0;

    std::cin >> n;

    while (n != 0) {
        sum += n % 10;
        n /= 10;
    }
    std::cout << sum << std::endl;

    return 0;
}

```

___
# D
Вашей программе подается на вход целое число n. Посчитайте сумму квадратов.

**Формат ввода

Целое число n (1 ≤ n ≤ 106). 

```c++
#include <iostream>

int main() {
    long long unsigned int n = 0;
    std::cin >> n;
    long long unsigned int s = (2 * n * n * n + 3 * n * n + n) / 6;
    std::cout << s << std::endl;
    return 0;
}

```

___
# E
По данному числу n вычислите сумму тут бла-бла-бла и логарифм 2. Операцией возведения в степень пользоваться нельзя. Алгоритм должен иметь сложность O(n). Попробуйте также обойтись без использования инструкции if. 

**Формат ввода**

Вводится натуральное число n, не превосходящее 106. 

**Формат вывода**

Выведите ответ на задачу. 
```c++

```

___
# F
Выведите все символы ASCII с кодами от 33 до 126 и их десятичные коды через пробел в следующем виде:
символ1 код1
символ2 код2
символ3 код3
...

Например, первая строчка должна быть такой:
! 33
```c++
#include <iostream>

int main() {
    for (int i = 33; i <= 126; i++) {
        std::cout << char(i) << ' ' << i << std::endl;
    }
}
```


___
# G
Вася хочет поменять свой пароль от электронной почты, потому что боится, что его ящик мог быть взломан. По правилам новый пароль должен удовлетворять таким ограничениям:

    состоять из символов таблицы ASCII с кодами от 33 до 126;
    быть не меньше 8 символов и не длиннее 14;
    из 4 классов символов — большие буквы, маленькие буквы, цифры, прочие символы — в пароле должны присутствовать не менее трёх любых.

Помогите Васе написать программу, которая проверит, что его новый пароль годится.

**Формат ввода**

На входе дана одна строка — новый Васин пароль.

**Формат вывода**

Выведите YES, если Васин пароль удовлетворяет требованиям, и NO в противном случае.
```c++
#include <iostream>
#include <string>

int main() {
    std::string pass;
    getline(std::cin, pass);
    bool good = true;

    if (pass.length() < 8 || (pass.length() > 14)) {
        good = false;
    }
    int large = 0;
    int small = 0;
    int number = 0;
    int other = 0;

    for (long unsigned int i = 0; i < pass.length(); i++) {
        int c = pass[i];
        if ((c < 33) || (c >127)) {
            good = false;
        }
        if ((c > 64) && (c < 91)) {
            large = 1;
        }
        if ((c > 96) && (c < 123)) {
            small = 1;
        }
        if ((c > 47) && (c < 58)) {
            number = 1;
        }
        bool a = (c > 32) && (c < 48);
        bool b = (c > 57) && (c < 65);
        bool e = (c > 90) && (c < 97);
        bool d = (c > 122) && (c < 128);
        bool g = a || b || e || d;

        if (g) {
            other = 1;
        }
    }

    if (small + large + number + other < 3) {
        good = false;
    }

    if (good == true) {
        std::cout << "YES";
    } else {
        std::cout << "NO";
    }

    return 0;
}
```

___
# H
Известный алгоритм Soundex (https://ru.wikipedia.org/wiki/Soundex) определяет, похожи ли два английских слова по звучанию. На вход он принимает слово и заменяет его на некоторый четырёхсимвольный код. Если коды двух слов совпадают, то слова, как правило, звучат похоже.

Вам требуется реализовать этот алгоритм. Он работает так:

    Первая буква слова сохраняется.
    В остальной части слова:
        буквы, обозначающие, как правило, гласные звуки: a, e, h, i, o, u, w и y — отбрасываются;
        оставшиеся буквы (согласные) заменяются на цифры от 1 до 6, причём похожим по звучанию буквам соответствуют одинаковые цифры:
        1: b, f, p, v
        2: c, g, j, k, q, s, x, z
        3: d, t
        4: l
        5: m, n
        6: r
    Любая последовательность одинаковых цифр сокращается до одной такой цифры.
    Итоговая строка обрезается до первых четырёх символов. Если длина строки меньше требуемой, недостающие символы заменяются знаком 0.

Примеры:
аmmonium → ammnm → a5555 → a5 → a500
implementation → implmnttn → i51455335 → i514535 → i514

**Формат ввода**

На вход подаётся одно непустое слово, записанное строчными латинскими буквами. Длина слова не превосходит 20 символов.

**Формат вывода**

Напечатайте четырёхбуквенный код, соответствующий слову.
```c++
#include <iostream>
#include <string>
#include <cstring>

int main() {
    std::string str, str1;
    getline(std::cin, str);
    int n;
    n = str.length();

    for (int i = 1; i < n; ++i) {
        if ((str[i] == 'a') ||
             (str[i] == 'e') ||
             (str[i] == 'h') ||
             (str[i] == 'i') ||
             (str[i] == 'o') ||
             (str[i] == 'u') ||
             (str[i] == 'w') ||
             (str[i] == 'y') ||
             (str[i] == 'A') ||
             (str[i] == 'E') ||
             (str[i] == 'H') ||
             (str[i] == 'I') ||
             (str[i] == 'O') ||
             (str[i] == 'U') ||
             (str[i] == 'W') ||
             (str[i] == 'Y')) {
            str.erase(i, 1);
            i--;
        }
    }

    str1 = str[0];

    for (long unsigned int i = 1; i < str.length(); ++i) {
        if ((str[i] == 'b') ||
             (str[i] == 'f') ||
             (str[i] == 'p') ||
             (str[i] == 'v') ||
             (str[i] == 'B') ||
             (str[i] == 'F') ||
             (str[i] == 'P') ||
             (str[i] == 'V')) {
            if (str[i-1] != '1') {
                str1 += '1';
            }
            str[i] = '1';
        } else if ((str[i] == 'c') ||
                   (str[i] == 'g') ||
                   (str[i] == 'j') ||
                   (str[i] == 'k') ||
                   (str[i] == 'q') ||
                   (str[i] == 's') ||
                   (str[i] == 'x') ||
                   (str[i] == 'z') ||
                   (str[i] == 'C') ||
                   (str[i] == 'G') ||
                   (str[i] == 'J') ||
                   (str[i] == 'K') ||
                   (str[i] == 'Q') ||
                   (str[i] == 'S') ||
                   (str[i] == 'X') ||
                   (str[i] == 'Z')) {
            if (str[i-1] != '2') {
                str1 += '2';
            }
            str[i] = '2';
        } else if ((str[i] == 'd') ||
                    (str[i] == 't') ||
                    (str[i] == 'D') ||
                    (str[i] == 'T')) {
            if (str[i-1] != '3') {
                str1 += '3';
            }
            str[i] = '3';
        } else if ((str[i] == 'l') ||
                    (str[i] == 'L')) {
            if (str[i-1] != '4') {
                str1 += '4';
            }
            str[i] = '4';
        } else if  ((str[i] == 'm') ||
                     (str[i] == 'n') ||
                     (str[i] == 'M') ||
                     (str[i] == 'N')) {
            if (str[i-1] != '5') {
                str1 += '5';
            }
            str[i] = '5';
        } else if ((str[i] == 'r') ||
                    (str[i] == 'R')) {
            if (str[i-1] != '6') {
                str1 += '6';
            }
            str[i] = '6';
        }
    }

    if (str1.length() >= 4) {
        std::cout << str1[0] << str1[1] << str1[2] << str1[3];
    } else if (str1.length() == 3) {
        std::cout << str1[0] << str1[1] << str1[2] << '0';
    } else if (str1.length() == 2) {
        std::cout << str1[0] << str1[1] << '0' << '0';
    } else if (str1.length() == 1) {
        std::cout << str1[0] << '0' << '0' << '0';
    }

    return 0;
}
```

___
# I
Дана строка, состоящая из строчных латинских букв и пробелов. Проверьте, является ли она палиндромом без учета пробелов (например, "argentina manit negra").

**Формат ввода**

На вход подается 1 строка длины не более 100, возможно содержащая пробелы. Подряд может идти произвольное число пробелов.

**Формат вывода**

Необходимо вывести yes, если данная строка является палиндромом, и no в противном случае. 
```c++
#include <iostream>
#include <algorithm>
#include <string>

int main() {
    std::string str, temp;
    getline(std::cin, str);
    str.erase(std::remove(str.begin(), str.end(), ' '), str.end());

    temp = str;

    std::reverse(str.begin(), str.end());
    if (temp == str) {
            std::cout << "yes" << std::endl;
    } else {
            std::cout << "no" << std::endl;
    }
    return 0;
}
```


___
# J
Напишите программу, которая прибавляет 1 к натуральному числу N (длина числа N до 1000 знаков)

**Формат ввода**

Дано чиcло N.

**Формат вывода**

Выведите число N+1. 
```c++
#include <iostream>
#include <string>

int main() {
    std::string number;
    getline(std::cin, number);
    long unsigned int i = 1;
    while (number[number.length() - i] == '9' && i <= number.length()) {
        number[number.length() - i] = '0';
        ++i;
    }
    if (i <= number.length()) {
        number[number.length() - i] += 1;
    } else {
        number = '1' + number;
    }
    std::cout << number;
    return 0;
}
```


___
# L
По данной перестановке требуется найти .

**Формат ввода**

В первой строке  входных данных содержится число 0 < N <= 20000 – количество элементов в перестановке . Во второй строке записана сама перестановка .

**Формат вывода**

Выведите обратную
```c++
#include <iostream>
#include <algorithm>
#include <vector>

int main() {
    int n;
    std::cin >> n;

    std::vector<int> v(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> v[i];
    }
    std::vector<int> cnt(n);
    for (int i = 0; i < n; ++i) {
        cnt[v[i]-1] = i+1;
    }

    for (int i = 0; i < n; ++i) {
        std::cout << cnt[i] << ' ';
    }
    return 0;
}
```

___
# M
Дан файл. Определите сколько в нем букв (латинского алфавита), слов, строк. Выведите три найденных числа в формате, приведенном в примере. Строки можно посчитать через количество срабатываний std::getline. Словом считается последовательность из подряд идущих букв латинского алфавита. 
```c++
#include <fstream>
#include <iostream>
#include <string>

int main() {
    int num_words = 0;
    int num_letters = 0;
    int num_strings = 0;
    bool F = false;
    std::ifstream file("input.txt");
    char current;
    while (file) {
        current = file.get();
        if (current == EOF) {
            break;
        } else {
            if (isalpha(current)) {
                ++num_letters;
                F = true;
            } else {
                if (F == true) {
                    ++num_words;
                    F = false;
                }
            }

            if (current == '\n') {
                num_strings++;
            }
        }
    }
    file.close();
    std::cout<< "Input file contains:" << "\n";
    std::cout << num_letters << " letters" << "\n";
    std::cout << num_words << " words" << "\n";
    std::cout << num_strings << " lines" << "\n";
    return 0;
}
```
