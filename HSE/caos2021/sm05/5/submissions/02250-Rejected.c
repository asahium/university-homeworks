// Comment by Judge: Строка 4
// Строка 6 - magic numbers, вынесите константы в отдельный enum
// 
// 
// Строка 6
// Строка 7
// Строка 9
// Не анализируются значения -1, которые могут вернуть системные вызовы
// 
// Строка 7
// Строка 9
// Избавьтесь от дублирования кода (достаточно одного вызова write в программе)



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
