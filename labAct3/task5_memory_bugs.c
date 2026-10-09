#include <stdio.h>
#include <stdlib.h>
void trigger_use_after_free(void) {
int *data = (int*)malloc(sizeof(int) * 5);
data[0] = 100;
free(data); // Memory returned to OS/allocator
// Bug: Temporal memory hazard (Dangling pointer write)
printf("Accessing freed memory: %d\n", data[0]);
}
int main(void) {
trigger_use_after_free();
return 0;
}