#include <bits/stdc++.h>
using namespace std;

void decoding(vector<int> op) {
    unordered_map<int, string> table;
    for (int i = 0; i <= 255; i++) {
        string ch = "";
        ch += char(i);
        table[i] = ch;
    }
    int old = op[0], n;
    string s = table[old];
    string c = "";
    c += s[0];
    cout << s;
    int count = 256;
    for (int i = 0; i < op.size() - 1; i++) {
        n = op[i + 1];
        if (table.find(n) == table.end()) {
            s = table[old];
            s = s + c;
        } else {
            s = table[n];
        }
        cout << s;
        c = "";
        c += s[0];
        table[count] = table[old] + c;
        count++;
        old = n;
    }
}
int main() {
    int size_code;
    std::cin >> size_code;
    std::vector<int> input_code;

    for (int i = 0; i < size_code; i++) {
        cin >> input_code[i];
    }
    decoding(input_code);
}