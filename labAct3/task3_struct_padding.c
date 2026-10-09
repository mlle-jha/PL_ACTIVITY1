#include <stdio.h>
#include <stddef.h>
// Unoptimized Layout: Interleaved types trigger hardware alignment padding
struct UnoptimizedData {
char a; // 1 byte

double b; // 8 bytes
char c; // 1 byte
int d; // 4 bytes
short e; // 2 bytes
};
// Optimized Layout: Order fields from largest to smallest alignment boundary
struct OptimizedData {
double b; // 8 bytes
int d; // 4 bytes
short e; // 2 bytes
char a; // 1 byte
char c; // 1 byte
};
int main(void) {
printf("========= STRUCT PADDING & ALIGNMENT ANALYSIS =========\n");
printf("[UnoptimizedData] Total Size: %zu bytes (Raw data: 16 bytes)\n", sizeof(struct
UnoptimizedData));
printf(" Offset of 'a' (char) : byte %zu\n", offsetof(struct UnoptimizedData, a));
printf(" Offset of 'b' (double) : byte %zu\n", offsetof(struct UnoptimizedData, b));
printf(" Offset of 'c' (char) : byte %zu\n", offsetof(struct UnoptimizedData, c));
printf(" Offset of 'd' (int) : byte %zu\n", offsetof(struct UnoptimizedData, d));
printf(" Offset of 'e' (short) : byte %zu\n", offsetof(struct UnoptimizedData, e));
printf("-------------------------------------------------------\n");
printf("[OptimizedData] Total Size: %zu bytes (Raw data: 16 bytes)\n", sizeof(struct OptimizedData));
printf(" Offset of 'b' (double) : byte %zu\n", offsetof(struct OptimizedData, b));
printf(" Offset of 'd' (int) : byte %zu\n", offsetof(struct OptimizedData, d));
printf(" Offset of 'e' (short) : byte %zu\n", offsetof(struct OptimizedData, e));
printf(" Offset of 'a' (char) : byte %zu\n", offsetof(struct OptimizedData, a));
printf(" Offset of 'c' (char) : byte %zu\n", offsetof(struct OptimizedData, c));
printf("=======================================================\n");
return 0;
}