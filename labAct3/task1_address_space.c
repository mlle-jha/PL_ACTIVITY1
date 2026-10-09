#include <stdio.h>
#include <stdlib.h>
// 1. Initialized Global Data Segment
int global_initialized_var = 42;
// 2. Uninitialized BSS Segment
int global_uninitialized_var;
void recursive_stack_growth(int depth) {
int local_stack_var = depth;
printf(" [Stack Frame %d] local_stack_var address: %p\n", depth, (void*)&local_stack_var);
if (depth < 3) {
recursive_stack_growth(depth + 1);
}
}
int main(void) {
// 3. Code/Text Segment
void (*code_ptr)(int) = recursive_stack_growth;
// 4. Heap Allocations
int *heap_chunk_1 = (int*)malloc(sizeof(int) * 100);
int *heap_chunk_2 = (int*)malloc(sizeof(int) * 100);
// 5. Stack Variables
int main_local_1 = 10;
int main_local_2 = 20;
printf("================ PROCESS MEMORY MAP ================\n");
printf("[Code / Text Segment] Function Pointer : %p\n", (void*)code_ptr);
printf("[Data Segment] Initialized Global : %p\n", (void*)&global_initialized_var);
printf("[BSS Segment] Uninitialized Var : %p\n", (void*)&global_uninitialized_var);
printf("----------------------------------------------------\n");
printf("[Heap Chunk 1] malloc Block 1 : %p\n", (void*)heap_chunk_1);
printf("[Heap Chunk 2] malloc Block 2 : %p\n", (void*)heap_chunk_2);
printf("----------------------------------------------------\n");
printf("[Main Stack Frame] main_local_1 : %p\n", (void*)&main_local_1);
printf("[Main Stack Frame] main_local_2 : %p\n", (void*)&main_local_2);
printf("----------------------------------------------------\n");
printf("Stack Frame Recursion Test:\n");
recursive_stack_growth(1);
printf("====================================================\n");
free(heap_chunk_1);
free(heap_chunk_2);
return 0;
}