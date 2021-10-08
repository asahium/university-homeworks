#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <functional>

using namespace std;

int n, m, k;
int cur_m;
bool fl;
vector<set<int> > graph;
set<pair<int, int>, greater<pair<int, int> > > que;
vector<int> answer;


void add(int ind) {
    answer.push_back(ind);
    cur_m += graph[ind].size();
    que.erase({graph[ind].size(), ind});

    for(auto t : graph[ind]) {
        int newind = t;
        auto p = que.find({graph[newind].size(), newind});
        if(p != que.end()) {
            que.erase({graph[newind].size(), newind});
            graph[newind].erase(ind);
            que.insert({graph[newind].size(), newind});
        }
    }
}

void del(int ind) {
    answer.pop_back();
    cur_m -= graph[ind].size();
    que.insert({graph[ind].size(), ind});

    for(auto t : graph[ind]) {
        int newind = t;
        auto p = que.find({graph[newind].size(), newind});
        if(p != que.end()) {
            que.erase({graph[newind].size(), newind});
            graph[newind].insert(ind);
            que.insert({graph[newind].size(), newind});
        }
    }
}

void make_output() {
    sort(answer.begin(), answer.end());
    cout << "Yes\n";
    for(int i = 0; i < answer.size(); ++i) {
        cout << answer[i] + 1 << ' ';
    }
    exit(0);
}

void perebor() {
    if(answer.size() > k)
        return;
    if(cur_m == m) {
        make_output();
        return;
    }

    int siz = que.begin()->first, ind = que.begin()->second;
    //left path
    add(ind);
    perebor();
    del(ind);

    //right path
    if(siz > 2) {
        vector<int> temp = {graph[ind].begin(), graph[ind].end()};
        for (auto t : temp) {
            add(t);
        }
        reverse(temp.begin(), temp.end());
        perebor();
        for (auto t : temp) {
            del(t);
        }
    }
    //otkat
}


int main() {
    cin >> n >> m >> k;
    cur_m = 0;
    fl = false;
    graph.resize(n);

    for(int i = 0, x, y; i < m; ++i) {
        cin >> x >> y;
        --x, --y;
        graph[x].insert(y);
        graph[y].insert(x);
    }

    for(int i = 0; i < n; ++i) {
        que.insert({graph[i].size(), i});
    }

    while(k && !que.empty()) {
        auto p = que.end();
        --p;
        int siz = p->first, ind = p->second;
        if(siz == 1) {
            add(*graph[ind].begin());
        }
        else {
            break;
        }
    }

    while(k && !que.empty()) {
        int siz = que.begin()->first, ind = que.begin()->second;
        if (siz > k) {
            add(ind);
        }
        else {
            break;
        }
    }

    perebor();

    cout << "No\n";
    return 0;
}
