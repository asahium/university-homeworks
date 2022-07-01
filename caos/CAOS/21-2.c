/* Взято с семинара 194 группы */
#include <stdio.h>
#include <sys/types.h>
#include <pthread.h>

void * thread_func(void * ptr) {
	int cnt;
	if (scanf("%d", &cnt) == 1) {
		pthread_t thread;
		pthread_create(&thread, NULL, thread_func, NULL);
		pthread_join(thread, NULL);
		printf("%d\n", cnt);
	}
	return NULL;
}

int main(void) {
	pthread_t thread;
	pthread_create(&thread, NULL, thread_func, NULL);
	pthread_join(thread, NULL);
}
