#include <stdio.h>
#include <pthread.h>

int amelie_bot(int previous_round[3]);
int bruce_bot(int previous_round[3]);
int charlotte_bot(int previous_round[3]);

struct thr {
    pthread_t id;
    int (*fun)(int [3]);
    int ans;
    int a[3];
    
};

void *func(void *arg) {
    struct thr *cur = arg;
    int result = cur->fun(cur->a);
    cur->ans = result;
    return NULL;
}

int main() {
    int n;
    if (scanf("%d", &n) < 0) {
        return 1;
    }
    int game[3];
    for (int i = 0; i < 3; ++i) {
        game[i] = 0;
    }
    struct thr thread[3];
    for (int i = 0; i < n; ++i) {
        thread[0].fun = amelie_bot;
        thread[1].fun = bruce_bot;
        thread[2].fun = charlotte_bot;
        for (int j = 0; j < 3; ++j) {
            for (int k = 0; k < 3; ++k) {
                thread[j].a[k] = game[k];
            }
            pthread_create(&thread[j].id, NULL, func, &thread[j]);
        }
        
        for (int j = 0; j < 3; ++j) {
            pthread_join(thread[j].id, NULL);
        }
        
        for (int j = 0; j < 3; ++j) {
            game[j] = thread[j].ans;
        }
        printf("%d %d %d %d\n", i + 1, game[0], game[1], game[2]);
    }
    return 0;
}
