Неизвестный водитель совершил ДТП и скрылся с места происшествия. Полиция опрашивает свидетелей. Каждый из них говорит, что запомнил какие-то буквы и цифры номера. Но при этом свидетели не помнят порядок этих цифр и букв. Полиция хочет проверить несколько подозреваемых автомобилей. Будем говорить, что номер согласуется с показанием свидетеля, если все символы, которые назвал свидетель, присутствуют в этом номере (не важно, сколько раз).

Формат ввода
Сначала задано число  - количество свидетелей. Далее идет M строк, каждая из которых описывает показания очередного свидетеля. Эти строки непустые и состоят из не более чем 20 символов. Каждый символ в строке - либо цифра, либо заглавная латинская буква, причём символы могут повторяться. 
Затем идёт число  - количество номеров. Следующие строки представляют из себя номера подозреваемых машин и имеют такой же формат, как и показания свидетелей.

Формат вывода
Выпишите номера автомобилей, согласующиеся с максимальным количеством свидетелей. Если таких номеров несколько, то выведите их в том же порядке, в котором они были заданы на входе.


#include <iostream>
#include <vector>
#include <algorithm>


using namespace std;


int main() {
    string s;
    int n;
    cin >> n;
    vector<string> sv(n);
    for(int i = 0; i < n; i++) {
        string ss;
        cin >> ss;
        sv[i] = ss;
    }
    int k;
    cin >> k;
    int maxx = 0;
    vector<string> num(k);
    vector<int> ans(k, 0);
    for (int j = 0; j < k; j++) {
        string ss;
        cin >> ss;
        num[j] = ss;
        for(size_t i = 0; i < n; i++) {
            bool l = true;
            for(const auto& it : sv[i]) {
                if (find(ss.begin(), ss.end(), it) == ss.end()) {
                    l = false;
                    break;
                }
            }
            if (l) {
                ans[j]++;
                if (ans[j] > maxx) {
                    maxx = ans[j];

                }
            }
        }
    }
    for(size_t i = 0; i < k; i++) {
        if (ans[i] == maxx) {
            cout << num[i] << "\n";
        }
    }
    return 0;
}