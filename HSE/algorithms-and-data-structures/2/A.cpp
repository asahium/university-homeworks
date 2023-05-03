#include <iostream>
#include <string>
#include <vector>

std::vector<int> prefix_function(const std::string& s) {
    std::vector<int> pi(s.length(), 0);
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
    std::string s;
    std::cin >> s;

    std::vector<int> pi = prefix_function(s);
    for (int i = 0; i < s.length(); ++i) {
        std::cout << pi[i] << " ";
    }
    return 0;
}