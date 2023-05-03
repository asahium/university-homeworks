// Total tests: 6
// Failed tests:
// 1 - Run-time error
// 2 - Run-time error
// 3 - Run-time error
// 4 - Run-time error
// 5 - Run-time error
// 6 - Run-time error



#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <sys/wait.h>
#include <stdio.h>

int main(int argc, char*argv[]) {
    assert(argc == 3);
    int fd[2];
    
    if (pipe(fd) == -1) {
        return 1;
    }
    
    int childpid = fork();
    assert(childpid != -1);
    
    if(childpid == 0) {
        close(fd[0]);
        
        dprintf(fd[1], "%s", argv[1]);
        int status;
        wait(&status);
        if (WIFEXITED(status)) {
            printf("%d\n", WEXITSTATUS(status));
        } else  if (WIFSIGNALED(status)) {
            printf("%d\n", -WTERMSIG(status));
        }
    } else {
        close(fd[1]);
        dup2(fd[0], STDIN_FILENO);
        close(fd[1]);
        execl(argv[2], argv[2], NULL);
        _exit(1);
    }
}
