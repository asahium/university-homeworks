Преподаватель Васиной группы наконец-то начал объявлять оценки за прошедшие работы. Так как важен не набор оценок, а средняя, то после каждого объявления студент, которому сообщили новую оценку, хочет знать среднее своих оценок по уже объявленным работам. Напишите программу, которая избавит Васиных одногруппников от лишнего ручного счета.

Формат ввода
Первая строка входного файла - целое число N от 0 до 105 - общеее количество оценок.

Далее идут N строк, каждая из которых содержит фамилию очередного студента (строка из латинских букв длиной от 1 до 20 символов) и его оценку - целое число от 0 до 109.

Формат вывода
Выведите N строк. k-я строка должна содержать среднюю оценку студента, которому была выставлена k-я оценка в исходном списке, после объявления k оценок. Средняя оценка округляется до ближайшего целого вниз (то есть, от нее отбрасывается дробная часть).

#include <iostream>
#include <map>


using namespace std;


int main() {
    int n;
    cin >> n;
    map<string, pair<long long, int>> m;
    for(int i = 0; i < n; i++) {
        string s;
        int x;
        cin >> s >> x;
        m[s].second++;
        m[s].first += x;
        cout << m[s].first / m[s].second << "\n";
    }
    return 0;
}