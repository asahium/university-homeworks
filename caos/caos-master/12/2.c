#include <unistd.h>

void copy_file(int in_fd, int out_fd) {
    char buf[4096];
    ssize_t read_res;
    ssize_t write_res;

    while ((read_res = read(in_fd, buf, 4096)) > 0) {
        write_res = write(out_fd, buf, read_res);

        while (write_res < read_res)
            write_res += write(out_fd, buf + write_res, read_res - write_res);
    }
}
