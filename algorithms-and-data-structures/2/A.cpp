#include <bits/stdc++.h>

using namespace std;

vector<int> prefix_function(const string& s) {
    vector<int> pi(s.length(), 0);

    for (int i = 1; i < s.length(); i++) {
        int j = pi[i - 1];

        while (j > 0 && s[i] != s[j]) {
            j = pi[j - 1];
        }

        if (s[i] == s[j]) {
            pi[i] = j + 1;
        } else {
            pi[i] = j;
        }
    }

    return pi;
}

int main() {
    string s, t;
    cin >> s >> t;

    vector<int> pi = prefix_function(s);
    for (int i = 0; i < s.length(); ++i) {
        cout << pi[i] << " ";
    }
    int t_len = t.length();

    for (int i = 0; i < s.length(); i++) {
        if (pi[t_len + 1 + i] == t_len) {
            cout << "s[" << i - t_len + 1 << ".." << i << "] = t" << "\n";
        }
    }
}