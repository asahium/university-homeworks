#include <unistd.h>

void copy_file(int in_fd, int out_fd) {
    char buffer[4096];
    ssize_t rres, wres;
    while ((rres = read(in_fd, buffer, 4096)) > 0) {
        wres = write(out_fd, buffer, rres);
        while (wres < rres) {
            wres += write(out_fd, buffer + wres, rres - wres);
        }
    }
}