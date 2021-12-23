#include <unistd.h>

void copy_file(int in_fd, int out_fd) {
    char buffer[4096];
    ssize_t read_res, write_res;
    while ((read_res = read(in_fd, buffer, 4096)) > 0) {
        write_res = write(out_fd, buffer, read_res);
        while (write_res < read_res) {
            write_res += write(out_fd, buffer + write_res, read_res - write_res);
        }
    }
}
