#include <sys/stat.h>

struct Task
{
    unsigned uid;
    int gid_count;
    unsigned *gids;
};

static int can(int mode, mode_t current, int w) {
    int r = (current >> (3 * mode)) & 7; 
    return (r & 1) >= (w & 1) && (r & 2) >= (w & 2) && (r & 4) >= (w & 4);
}

int myaccess(const struct stat *file, const struct Task *user, int a) {
    if (user->uid == 0)
        return 1;

    if (file->st_uid == user->uid)
        return can(2, file->st_mode, a);

    for (int i = 0; i < user->gid_count; ++i)
        if (user->gids[i] == file->st_gid)
            return can(1, file->st_mode, a);

    return can(0, file->st_mode, a);
}
