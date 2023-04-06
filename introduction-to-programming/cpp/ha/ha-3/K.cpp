Преподаватель Алексей собрался подвести итоги модуля и выставить студентам накопленные оценки. Он скачал из Яндекс.Контеста файлы с итогами домашних и контрольных работ. В файлах построчно записаны логины студентов и набранные баллы. Если студент ничего не сдавал в данном контесте, то записи о нём не будет. В таком случае считается, что он получил за этот контест 0 баллов.

Напишите программу, строящую итоговую таблицу с результатами.

Формат ввода
В первой строке указано число N - количество контестов. Далее идет N блоков с данными, описывающими очередной контест. В каждом блоке сначала указано число Ki - количество студентов, сдававших i-й контест. Затем идет Ki строк. Сначала в строке указан логин студента (не содержащий пробелов), затем через пробел - его результат. Внутри одного блока все логины разные. Все числа (N, Ki и результаты студента) являются неотрицательными целыми и не превосходят 1000.

Формат вывода
Для каждого студента, сдававшего хотя бы один контест, выведите строку с его результатами. Сначала напечатайте его логин, а далее через табуляцию N чисел - результаты в каждом из контестов. Список студентов упорядочите в алфавитном порядке по логинам.

#include <iostream>
#include <map>
#include <vector>


using namespace std;


int main() {
    int n;
    cin >> n;
    map<string, vector<int>> m;
    for (int i = 0; i < n; i++) {
        int k;
        cin >> k;
        for (int j = 0; j < k; j++) {
            string s;
            int x;
            cin >> s >> x;
            if(m[s].size() < n){
                m[s].resize(n, 0);
            }
            m[s][i] = x;
        }
    }
    for (auto& [key, value] : m) {
        cout << key << "\t";
        for (auto v : value) {
            cout << v << "\t";
        }
        cout << "\n";
    }
    return 0;
}
