#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define MATRIX_SIZE 8192
// Allocate contiguous 2D array in heap (8192 x 8192 * 4 bytes = 256 MB)
int matrix[MATRIX_SIZE][MATRIX_SIZE];
int main(void) {
clock_t start, end;
long long sum = 0;

printf("Benchmarking 256 MB Matrix Traversal (%dx%d)...\n", MATRIX_SIZE, MATRIX_SIZE);
// 1. Row-Major Traversal (Cache-Friendly: Sequential memory strides)
start = clock();
for (int i = 0; i < MATRIX_SIZE; i++) {
for (int j = 0; j < MATRIX_SIZE; j++) {
sum += matrix[i][j];
}
}
end = clock();
double row_major_time = ((double)(end - start)) / CLOCKS_PER_SEC;
printf("[Row-Major Traversal] Time Elapsed: %.4f seconds\n", row_major_time);
// 2. Column-Major Traversal (Cache-Hostile: 32KB Stride jumps causing L1/L2 misses)
sum = 0;
start = clock();
for (int j = 0; j < MATRIX_SIZE; j++) {
for (int i = 0; i < MATRIX_SIZE; i++) {
sum += matrix[i][j];
}
}
end = clock();
double col_major_time = ((double)(end - start)) / CLOCKS_PER_SEC;
printf("[Column-Major Traversal] Time Elapsed: %.4f seconds\n", col_major_time);
printf("Performance Gap: Column-Major is %.2fx slower!\n", col_major_time / row_major_time);
return 0;
}