#include <sys/stat.h>

struct Task {
    unsigned uid;
    int gid_count;
    unsigned *gids;
};

static int permission(int code, mode_t mode, int a) {
    int b = (mode >> (3 * code)) & 0b111; 
    if (((b&0b100) >= (a&0b100)) && ((b&0b010) >= (a&0b010)) &&
    ((b&0b001) >= (a&0b001))) {
        return 1;
    }
    return 0;
}

int myaccess(const struct stat *stb, const struct Task *task, int access) {
    if (task->uid == 0) {
        return 1;
    }
    if (stb->st_uid == task->uid) {
        return permission(2, stb->st_mode, access);\
    }
    for (int i = 0; i < task->gid_count; ++i) {
        if (task->gids[i] == stb->st_gid) {
            return permission(1, stb->st_mode, access);
        }
    }
    return permission(0, stb->st_mode, access);
}