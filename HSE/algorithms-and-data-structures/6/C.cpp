#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <limits>
 
 
class FlowGraph {
public:
    void AddFlow(int x, int y, int delta);
    const int& GetFlow(int x, int y) const;
    const int& Size() const;
    FlowGraph(int n);
private:
    std::vector<int> buffer;
    int sz;
};
 
FlowGraph::FlowGraph(int n): sz(n), buffer(n * n, 0) {
 
}
 
const int& FlowGraph::Size() const {
    return sz;
}
 
void FlowGraph::AddFlow(int x, int y, int delta) {
    buffer[sz * x + y] += delta;
}
 
const int& FlowGraph::GetFlow(int x, int y) const {
    return buffer[sz * x + y];
}
 
int FixWay(const FlowGraph& graph, FlowGraph& flow, const int& s, const int& t, const std::vector<int>& parent) {
    int cur = t;
    int delta = -1;
    while (cur != s) {
        const int maxFlowForEdge = graph.GetFlow(parent[cur], cur) - flow.GetFlow(parent[cur], cur);
        delta = delta == -1 ? maxFlowForEdge : std::min(maxFlowForEdge, delta);
        cur = parent[cur];
    }
    cur =  t;
    while (cur != s) {
        flow.AddFlow(parent[cur], cur, delta);
        flow.AddFlow(cur, parent[cur], -delta);
        cur = parent[cur];
    }
    return delta;
}
 
int UpFlow (const FlowGraph& graph, FlowGraph& flow, int s, int t) {
    std::vector<int> parent(graph.Size(), -1);
    std::vector<bool> used(graph.Size(), false);
    std::queue<int> q;
    q.push(s);
    used[s] = true;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        if (v == t) {
            return FixWay(graph, flow, s, t, parent);
        }
        for (int i = 0; i < graph.Size(); ++i) {
            const int& maxFlow = graph.GetFlow(v, i);
            const int& curFlow = flow.GetFlow(v, i);
            if (!used[i] && maxFlow - curFlow > 0) {
                parent[i] = v;
                used[i] = true;
                q.push(i);
            }
        }
    }
    return 0;
}
 
int EdmondsKarp(const FlowGraph& g, int s, int t) {
    int res = 0;
    int delta = 0;
    FlowGraph f(g.Size());
    do {
        res += delta;
        delta = UpFlow(g, f, s, t);
    } while (delta > 0);
    return res;
}
 
FlowGraph ReadGraph() {
    int n, m;
    std::cin >> n >> m;
    FlowGraph g(n);
    for (int i = 0; i < m; ++i) {
        int x, y, w;
        std::cin >> x >> y >> w;
        --x; --y;
        g.AddFlow(x, y, w);
    }
    return g;
}
 
void Solve() {
    FlowGraph graph = ReadGraph();
    std::cout << EdmondsKarp(graph, 0, graph.Size() - 1) << std::endl;
}
 
int main() {
    Solve();
}
