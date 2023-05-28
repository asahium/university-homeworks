// В данной задаче Вам необходимо решить классическую задачу о рюкзаке.
//
// Формат ввода
// Количество предметов
// Веса предметов
// Ценность предметов
// Размер рюкзака
//
// Формат вывода
// Вес оптимального рюкзака и его ценность через пробел

#include <iostream>
#include <vector>

int knapsack(const std::vector<int>& prices, const std::vector<int>& weights, int itemCount, int maxWeight) {
    std::vector<std::vector<int>> dp(2, std::vector<int>(maxWeight + 1));

    for (int i = 0; i < itemCount; ++i) {
        if (i % 2 != 0) {
            for (int j = 0; j <= maxWeight; ++j) {
                if (weights[i] <= j) {
                    dp[1][j] = std::max(prices[i] + dp[0][j - weights[i]], dp[0][j]);
                } else {
                    dp[1][j] = dp[0][j];
                }
            }
        } else {
            for (int j = 0; j <= maxWeight; ++j) {
                if (weights[i] <= j) {
                    dp[0][j] = std::max(prices[i] + dp[1][j - weights[i]], dp[1][j]);
                } else {
                    dp[0][j] = dp[1][j];
                }
            }
        }
    }

    return (itemCount % 2 != 0) ? dp[0][maxWeight] : dp[1][maxWeight];
}

int main() {
    int itemCount = 0;
    int maxWeight = 0;

    std::cin >> itemCount;

    std::vector<int> weights(itemCount);
    std::vector<int> prices(itemCount);

    for (int i = 0; i < itemCount; ++i) {
        std::cin >> weights[i];
    }

    for (int i = 0; i < itemCount; ++i) {
        std::cin >> prices[i];
    }

    std::cin >> maxWeight;

    int result = knapsack(prices, weights, itemCount, maxWeight);

    std::cout << maxWeight << ' ' << result;

    return 0;
}
