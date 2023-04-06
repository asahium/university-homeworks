#include <iostream>
#include <vector>

size_t n, m;
std::vector<std::vector<int>> g;
std::vector<int> m;
std::vector<char> used;

bool kun(int u) {
    if (used[u]) {
        return false;
    }
    used[u] = true;
    for (int i = 0; i < g[u].size(); ++i) {
        int v = g[u][i];
        if (m[v] == -1 || kun(m[v])) {
            m[v] = u;
            return true;
        }
    }
    return false;
}

int main() {
    std::cin >> n >> m;
    g.resize(n);
    m.assign(m, -1);
    for (int i = 0; i < n; ++i) {
        int v;
        std::cin >> v;
        while (v != 0) {
            g[i].push_back(v - 1);
            std::cin >> v;
        }
    }

    for (int i = 0; i < n; ++i) {
        used.assign(n, false);
        kun(i);
    }

    int count = 0;
    for (int i = 0; i < m; ++i) {
        if (m[i] != -1) {
            count++;
        }
    }
    std::cout << count << "\n";

    for (int i = 0; i < m; ++i) {
        if (m[i] != -1) {
            std::cout << m[i] + 1 << " " << i + 1 << "\n";
        }
    }
    return 0;
}
