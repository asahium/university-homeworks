#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

using namespace std;

const int N = 1e3 + 1;

void make_tr(vector<vector<int> >& g, vector<vector<int> >& tr_g) {
    tr_g.assign(g.size(), vector<int>(0));
    for (int i = 0; i < g.size(); ++i)
        for (int j = 0; j < g[i].size(); ++j) {
            int to = g[i][j];
            tr_g[to].push_back(i);
        }
}

//a pochemu net

int form(char t) {
    if (t == 'R')
        return 0;
    if (t == 'B')
        return 1;
    if (t == 'G')
        return 2;
    return 3;
}

char form(int t) {
    if (t == 0)
        return 'R';
    if (t == 1)
        return 'B';
    if (t == 2)
        return 'G';
    return 'X';
}

vector<int> order;

void dfs(int v, vector<vector<int> >& g, vector<int>& used, int color = 0) {
    used[v] = max(color, 1);
    for (int i = 0; i < g[v].size(); ++i) {
        int to = g[v][i];
        if (!used[to]) {
            dfs(to, g, used, color);
        }
    }
    if (color == 0) {
        order.push_back(v);
    }
}

int main() {
    int n, m;
    cin >> n >> m;

    string s;
    cin >> s;

    int color[N][2];
    vector<vector<int> > sat_g(2 * n), tr_g;

    for (int i = 0; i < n; ++i) {
        int col = form(s[i]), l = 0;
        for (int c = 0; c < 3; ++c) {
            if (c != col) {
                color[i][l] = c;
                ++l;
            }
        }
    }

    for (int i = 0; i < m; ++i) {
        int x, y;
        cin >> x >> y;
        --x, --y;
        for (int cx = 0; cx < 2; ++cx)
            for (int cy = 0; cy < 2; ++cy)
                if (color[x][cx] == color[y][cy]) {
                    sat_g[x + cx * n].push_back(y + (cy + 1) % 2 * n);
                    sat_g[y + cy * n].push_back(x + (cx + 1) % 2 * n);
                }
    }

    make_tr(sat_g, tr_g);
    vector<int> used(2 * n);

    for (int i = 0; i < 2 * n; ++i) {
        if (!used[i])
            dfs(i, tr_g, used);
    }

    int t = 0;
    used.assign(2 * n, 0);
    reverse(order.begin(), order.end());
    for (int i = 0; i < 2 * n; ++i) {
        int v = order[i];
        if (!used[v]) {
            ++t;
            dfs(v, sat_g, used, t);
        }
    }

    string answer;
    for (int i = 0; i < n; ++i) {
        if (used[i] == used[i + n]) {
            cout << "Impossible";
            return 0;
        }
        if (used[i] < used[i + n]) {
            answer.push_back(form(color[i][0]));
        }
        else
            answer.push_back(form(color[i][1]));
    }
    cout << answer;
    return 0;
}
