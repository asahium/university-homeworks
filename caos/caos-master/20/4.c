#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <inttypes.h>
#include <signal.h>
#include <bits/sigaction.h>
#include <signal.h>
#include <wait.h>
#include <sys/mman.h>

volatile int *__exit;

#define CONTINUE !*__exit
#define EIL(r) if (r < 0) _exit(0);
#define CHK(m) h_exit(m, read, write);
#define WTILL(reason)  while (waitpid(-1, NULL, reason) > 0);
#define SETSOCKVAR(var) setsockopt(socket_fd, SOL_SOCKET, var, &val, sizeof(val));

char * key;

int socket_fd;

struct sockaddr_in addr = {};
socklen_t addr_size;

void h_sigterm(int _) {
    (void)_;

    *__exit = 1;

    WTILL(0)

    munmap((void *) __exit, sizeof(int));

    _exit(0);
}

void h_sa() {
    struct sigaction sa = {
            .sa_handler = h_sigterm,
            .sa_flags = SA_RESTART
    };

    sigemptyset(&sa.sa_mask);
    sigaction(SIGTERM, &sa, NULL);
}

void h_socket() {
    socket_fd = socket(AF_INET, SOCK_STREAM, 0);

    EIL(socket_fd)

    int val = 1;

    SETSOCKVAR(SO_REUSEADDR)
    SETSOCKVAR(SO_REUSEPORT)
}

void h_bind_listen(char * port) {
    addr.sin_family = AF_INET;
    addr.sin_port = htons(atoi(port));
    addr.sin_addr.s_addr = INADDR_ANY;

    addr_size = sizeof(addr);

    EIL(bind(socket_fd, (struct sockaddr *) &addr, addr_size))
    EIL(listen(socket_fd, 5))
}

void h_exit_flag() {
    __exit = mmap(NULL, sizeof(int), PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANON, -1, 0);
    *__exit = 0;
}

void h_exit(int res, FILE * read, FILE * write) {
    fflush(write);

    if (res > 0 && CONTINUE)
        return;

    fclose(read);
    fclose(write);
    _exit(0);
}

void h_client_session(FILE *read, FILE *write, int serial) {
    CHK(fprintf(write, "%s\r\n", key))
    CHK(fprintf(write, "%d\r\n", serial))

    int max;
    CHK(fscanf(read, "%d", &max))
    CHK(fprintf(write, "%d\r\n", max))

    int sum;
    int num;

    while (CONTINUE) {
        CHK(fscanf(read, "%d", &num))

        if (num > max || __builtin_add_overflow(num, serial, &sum)) {
            CHK(fprintf(write, "-1\r\n"))
            break;
        }

        CHK(fprintf(write, "%d\r\n", num + serial))
    }

    fclose(read);
    fclose(write);
    _exit(0);
}

void h_connection(int serial) {
    WTILL(WNOHANG)

    int client_fd = accept(socket_fd, (struct sockaddr *) &addr, &addr_size);

    EIL(client_fd)

    if (!fork()) {
        int write_fd = dup(client_fd);

        h_client_session(fdopen(client_fd, "r"), fdopen(write_fd, "w"), serial);
    }

    close(client_fd);
}

int main(int argc, char **argv) {
    h_sa();

    key = argv[2];

    h_socket();

    h_bind_listen(argv[1]);

    h_exit_flag();

    int serial = 0;

    while (CONTINUE)
        h_connection(++serial);

    close(socket_fd);
}
