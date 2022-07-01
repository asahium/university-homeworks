#include <sys/socket.h>
#include <stdio.h>
#include <netdb.h>
#include <unistd.h>

struct addrinfo * result;

struct addrinfo hints = {
        .ai_family = PF_INET,
        .ai_socktype = SOCK_STREAM
};

int sfd;

FILE * in;
FILE * out;

void c_getaddrinfo(char * host, char * service) {
    if (getaddrinfo(host, service, &hints, &result) < 0)
        _exit(0);
}

void c_socket() {
    sfd = socket(result->ai_family, result->ai_socktype, 0);

    if (sfd < 0) {
        freeaddrinfo(result);
        _exit(0);
    }
}

void c_connect() {
    if (connect(sfd, result->ai_addr, result->ai_addrlen) < 0) {
        freeaddrinfo(result);
        _exit(0);
    }
}

void c_open_fd() {
    int sfd2 = dup(sfd);

    in = fdopen(sfd, "r");
    out = fdopen(sfd2, "w");
}

void c_print_key(char * key) {
    int res = fprintf(out, "%s\n", key);
    fflush(out);

    if (res < 0) {
        freeaddrinfo(result);
        _exit(0);
    }

}

int c_read_count() {
    int num;

    if (fscanf(in, "%d", &num) < 0) {
        freeaddrinfo(result);
        _exit(0);
    }

    return num;
}

void c_print_nums(int num) {
    int res;

    for (int i = 0; i <= num; ++i) {
        res = fprintf(out, "%d\n", i);
        fflush(out);

        if (res < 0) {
            freeaddrinfo(result);
            _exit(0);
        }
    }
}

void c_process_last() {
    unsigned long long value;

    if (fscanf(in, "%llu", &value) < 0) {
        freeaddrinfo(result);
        _exit(0);
    }

    printf("%llu\n", value);
    fflush(stdout);
}

int main(int _, char ** argv) {
    c_getaddrinfo(argv[1], argv[2]);

    c_socket();

    c_connect();
    c_open_fd();
    c_print_key(argv[3]);

    int num = c_read_count();

    c_print_nums(num);
    c_process_last();

    fclose(in);
    fclose(out);
    freeaddrinfo(result);
}