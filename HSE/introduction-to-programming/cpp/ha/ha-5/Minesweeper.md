### Условие


Вы играли когда-нибудь в компьютерную игру "Сапёр"?
https://ru.wikipedia.org/wiki/Сапёр_(игра)

В этой игре на прямоугольном поле расставлены мины. Вы должны разминировать поле. На каждой клетке, не занятой миной, написано, сколько мин расположено в клетках вокруг неё.

Один студент решил написать класс для своей реализации этой игры. Класс должен уметь создавать прямоугольное поле заданных размеров, ставить "мину" в указанную клетку (индексы клеток начинаются с нуля), а также записывать в каждую свободную клетку количество мин вокруг неё. Кроме того, должен быть оператор <<, который печатает поле (а вместо мин печатает "звездочки").

К сожалению, код студента содержит ошибки и не проходит тесты. Помогите ему исправить и сдать программу. Код студента доступен по адресу https://clck.ru/AP2QQ.
Примечания

Вам требуется сдать только исправленный код класса Minesweeper и оператора <<. Функции main в Вашем коде быть не должно. Ваша программа будет автоматически собрана с нашей функцией main примерно такого содержания: https://clck.ru/ABQDY.


### Решение


```cpp
#include <iostream>
#include <vector>

using std::vector;

class Minesweeper {
private:
    size_t M, N;
    vector<vector<int>> Table;

public:
    Minesweeper(size_t m, size_t n): M(m), N(n) {
        Table.resize(M);
        int i = 0;
        for (auto row : Table) {
            row.resize(N);
            Table[i] = row;
            i++;
        }
    }

    size_t Rows() {
        return M;
    }

    size_t Columns() {
        return N;
    }

    void SetMine(size_t i, size_t j) {
        Table[i][j] = -1;
    }

    int operator () (size_t i, size_t j) const {
        return Table[i][j];
    }

    void CheckForMinesAround() {
        for (size_t i = 0; i != M; ++i)
            for (size_t j = 0; j != N; ++j)
                if (Table[i][j] != -1)
                CheckForMinesAround(i, j);
    }

private:
    void CheckForMinesAround(size_t i, size_t j) {
        int counter = 0;
        for (int dx = -1; dx <= 1; ++dx) {
            for (int dy = -1; dy <= 1; ++dy)
                if (0 <= i + dx && i + dx < M &&
                    0 <= j + dy && j + dy < N &&
                    Table[i + dx][j + dy] == -1
                        ) {
                    ++counter;
                }
        }
        Table[i][j] = counter;
    }
};

std::ostream& operator << (std::ostream& out, Minesweeper& ms)  {
    for (size_t i = 0; i != ms.Rows(); ++i) {
        for (size_t j = 0; j != ms.Columns(); ++j)
            if (ms(i, j) == -1)
                out << '*';
            else
                out << ms(i, j);
        out << "\n";
    }
    return out;
}
```
