#include <stdio.h>
int compute_sum(int a, int b) {
int local_result = a + b;
return local_result;
}
int main(void) {
int x = 15;
int y = 25;
int total = compute_sum(x, y);
printf("Sum: %d\n", total);
return 0;
}