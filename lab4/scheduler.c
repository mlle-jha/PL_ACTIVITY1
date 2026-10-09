#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <limits.h>

typedef struct { int id; char title[32]; int priority; char due[11]; int done; } Task;

static Task *tasks; static int count = 0, next_id = 1;

static void add_task(const char *title, int priority, const char *due) {
    Task *t = &tasks[count++];
    t->id = next_id++; t->priority = priority; t->done = 0;
    strncpy(t->title, title, 31); t->title[31] = 0;
    strncpy(t->due, due, 10);     t->due[10] = 0;
}

static int cmp(const void *a, const void *b) {
    const Task *x = a, *y = b;
    if (x->priority != y->priority) return x->priority - y->priority;
    return strcmp(x->due, y->due);
}

static void complete(int id) { for (int i = 0; i < count; i++) if (tasks[i].id == id) tasks[i].done = 1; }

static void list(void) {
    qsort(tasks, count, sizeof(Task), cmp);
    for (int i = 0; i < count; i++)
        printf("  #%d [P%d] %-14s due %s %s\n", tasks[i].id, tasks[i].priority, tasks[i].title, tasks[i].due, tasks[i].done ? "(done)" : "");
}

int main(void) {
    tasks = malloc(sizeof(Task) * 200100);
    printf("C:\n");
    add_task("Deadline OS Project", 2, "2026-10-12");
    add_task("Pass PL Activity 4 & 5", 1, "2026-10-09");
    add_task("Remedial Quiz 5", 3, "2026-10-13");
    complete(2);
    list();

    printf("-- Type tests --\n");
    add_task("Bad", 2.9, "2026-10-20");        /* compiles: double -> int truncates to 2 */
    printf("  add_task(\"Bad\", 2.9)   -> stored priority = %d (silent truncation)\n", tasks[count-1].priority);
    add_task("Bad", 'A', "2026-10-20");        /* compiles: char -> int = 65 */
    printf("  add_task(\"Bad\", 'A')   -> stored priority = %d (char treated as int)\n", tasks[count-1].priority);
    add_task("Bad", atoi("abc"), "2026-10-20");/* atoi gives 0, no error */
    printf("  atoi(\"abc\")            -> %d (no error reported)\n", tasks[count-1].priority);
    int big = INT_MAX; big += 1;               /* signed overflow = undefined behavior */
    printf("  INT_MAX + 1            -> %d (undefined behavior)\n", big);
    
    printf("-- Benchmark --\n");
    count = 0; next_id = 1; srand(42);
    int n = 200000; char due[11], title[32];
    clock_t s = clock();
    for (int i = 0; i < n; i++) {
        snprintf(title, sizeof title, "t%d", i);
        snprintf(due, sizeof due, "2026-10-%02d", 10 + rand() % 18);
        add_task(title, rand() % 5, due);
    }
    qsort(tasks, count, sizeof(Task), cmp);
    printf("  %d tasks added+sorted in %.1f ms\n", n, (double)(clock() - s) * 1000 / CLOCKS_PER_SEC);
    free(tasks);
    return 0;
}