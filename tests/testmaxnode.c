
#include <stdio.h>

#include <genders.h>

int
main(void) {
    genders_t handle;
    int maxnode;

    handle = genders_handle_create();
    genders_load_data(handle, "test-data/genders");

    maxnode = genders_getmaxnodelen(handle);

    printf("maxnodelen: %d\n", maxnode);

    return 0;
    
}
