#include <stdio.h>
#include <stddef.h>

//Unoptimized Layout: Members are arranged in an interleaved order, which causes additional padding for alignment.
struct OldUnoptimizedData {
    char a;      // 1 byte
    double b;    // 8 bytes
    char c;      // 1 byte
    int d;       // 4 bytes
    short e;     // 2 bytes
};
//Optimized Layout: Members are arranged from largest to smallest alignment requirement to reduce padding.
struct NewOptimizedData {
    double b;    // 8 bytes
    int d;       // 4 bytes
    short e;     // 2 bytes
    char a;      // 1 byte
    char c;      // 1 byte
};

int main(void) {
    printf("========= STRUCT PADDING & ALIGNMENT ANALYSIS =========\n");
    printf("[OldUnoptimizedData] Total Size: %zu bytes (Raw data: 16 bytes)\n", sizeof(struct
    OldUnoptimizedData));
    printf(" Offset of 'a' (char) : byte %zu\n", offsetof(struct OldUnoptimizedData, a));
    printf(" Offset of 'b' (double) : byte %zu\n", offsetof(struct OldUnoptimizedData, b));
    printf(" Offset of 'c' (char) : byte %zu\n", offsetof(struct OldUnoptimizedData, c));
    printf(" Offset of 'd' (int) : byte %zu\n", offsetof(struct OldUnoptimizedData, d));
    printf(" Offset of 'e' (short) : byte %zu\n", offsetof(struct OldUnoptimizedData, e));
    printf("-------------------------------------------------------\n");
    printf("[NewOptimizedData] Total Size: %zu bytes (Raw data: 16 bytes)\n", sizeof(struct NewOptimizedData));
    printf(" Offset of 'b' (double) : byte %zu\n", offsetof(struct NewOptimizedData, b));
    printf(" Offset of 'd' (int) : byte %zu\n", offsetof(struct NewOptimizedData, d));
    printf(" Offset of 'e' (short) : byte %zu\n", offsetof(struct NewOptimizedData, e));
    printf(" Offset of 'a' (char) : byte %zu\n", offsetof(struct NewOptimizedData, a));
    printf(" Offset of 'c' (char) : byte %zu\n", offsetof(struct NewOptimizedData, c));
    printf("=======================================================\n");
    return 0;
}