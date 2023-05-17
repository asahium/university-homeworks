# В данной задаче Вам необходимо решить задачу упаковки ящиков (https://ru.wikipedia.org/wiki/Задача_об_упаковке_в_контейнеры).

# Формат ввода
# Количество предметов
# Веса предметов через пробел
# Вместимость одного ящика

# Формат вывода
# Минимальное количество ящиков, необходимое для упаковки всех предметов.


with open('input.txt') as f:
    n = int(f.readline())
    w = list(map(int, f.readline().split()))
    c = int(f.readline())

w.sort(reverse=True)
boxes = [c]
ans = 1

for i in range(n):
    no_flag = True
    for j in range(len(boxes)):
        if boxes[j] - w[i] >= 0:
            boxes[j] -= w[i]
            no_flag = False
            break
    if no_flag:
        boxes.append(c - w[i])
        ans += 1

print(ans)