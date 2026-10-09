#include <stdio.h>

int main() {
    int number = 10;
    if (number > 0) {
        printf("Positive.\n");
        if (number % 2 == 0) {
            printf("Even.\n");
        } else {
            printf("Odd.\n");
        }
    } else {
        printf("Negative.\n");
    }
    return 0;
}

void greet() {
    printf("Hello!");
}

