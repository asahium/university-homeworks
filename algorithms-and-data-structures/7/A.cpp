#include <bits/stdc++.h>
using namespace std;

bool check(int[][5], vector<int> &, int);

// Function to construct a set of given size k
bool func(int graph[][5], vector<int> &arr,
          int k, int index, bool sol[]) {
    // Check if the selected set is independent or not.
    // Change the value of sol to True and return
    // if it is independent
    if (k == 0) {
        if (check(graph, arr, arr.size())) {
            sol[0] = true;
            return true;
        }
    } else {
        // Set of size k can be formed even if we don't
        // include the vertex at current index.
        if (index >= k) {
            vector<int> newvec(arr.begin(), arr.end());
            newvec.push_back(index);
            return (func(graph, newvec, k - 1,
                                index - 1, sol) or
                    func(graph, arr, k, index - 1, sol));
        } else {
            arr.push_back(index);
            return func(graph, arr, k - 1,
                          index - 1, sol);
        }
    }
}

// Function to check if the given set is
// independent or not
// arr --> set of size k (contains the
// index of included vertex)
bool check(int graph[][5], vector<int> &arr, int n) {
    // Check if each vertex is connected to any other
    // vertex in the set or not
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (graph[arr[i]][arr[j]] == 1)
                return false;
    return true;
}

int main() {
    int graph[][5] = {{0, 1, 0, 0, 0},
                      {1, 0, 0, 0, 0},
                      {0, 0, 0, 1, 0},
                      {0, 0, 1, 0, 1},
                      {0, 0, 0, 1, 0}};
    int k = 4;
    vector<int> arr;
    bool sol[] = {false};
    int n = sizeof(graph) /
            sizeof(graph[0]);
    func(graph, arr, k, n - 1, sol);

    if (sol[0])
        cout << "Yes" << endl;
    else
        cout << "No" << endl;
    return 0;
}
