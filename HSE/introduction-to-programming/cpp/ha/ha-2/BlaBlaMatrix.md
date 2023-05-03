### Условие

Дан двумерный массив размером n × m (n, m < 1000). Симметричный ему относительно главной диагонали массив называется транспонированным к данному. Он имеет размеры m × n: строки исходного массива становятся столбцами транспонированного, столбцы исходного массива становятся строками транспонированного.

Для данного массива постройте транспонированный массив.

Решение оформите в виде функции:

std::vector<std::vector<int>> Transpose(const std::vector<std::vector<int>>& matrix).

Примечания

В вашей программе не должно быть функции main, а должна быть только функция Transpose и необходимые для её работы директивы #include. Мы при проверке соберём ваш код с нашей функцией main. 

### Решение
```cpp
#include <vector>

std::vector<std::vector<int>> Transpose(const std::vector<std::vector<int>>& matrix) {
    std::vector<std::vector<int>> mat(matrix[0].size(), std::vector<int> (matrix.size(), 0));
    for (long unsigned int i = 0; i < matrix.size(); ++i) {
        for (long unsigned int j = 0; j < matrix[0].size(); ++j)
            mat[j][i] = matrix[i][j];
    }
    return mat;
}
```
