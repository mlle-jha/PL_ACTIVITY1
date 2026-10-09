
import java.time.LocalDate;
import java.util.*;

public class scheduler {

    record Task(int id, String title, int priority, LocalDate due, boolean[] done) {}

    static List<Task> tasks = new ArrayList<>();
    static int nextId = 1;

    static Task addTask(String title, int priority, String due) {
        Task t = new Task(nextId++, title, priority, LocalDate.parse(due), new boolean[]{false});
        tasks.add(t);
        return t;
    }

    static void complete(int id) {
        for (Task t : tasks) {
            if (t.id() == id) {
                t.done()[0] = true;
            }
        }
    }

    static void list() {
        List<Task> sorted = new ArrayList<>(tasks);
        sorted.sort(Comparator.comparingInt(Task::priority).thenComparing(Task::due));
        for (Task t : sorted) {
            System.out.printf("  #%d [P%d] %-14s due %s %s%n", t.id(), t.priority(), t.title(), t.due(), t.done()[0] ? "(done)" : "");
        }
    }

    public static void main(String[] args) {
        System.out.println("Java:");
        addTask("Deadline OS Project", 2, "2026-10-12");
        addTask("Pass PL Activity 4 & 5", 1, "2026-10-09");
        addTask("Remedial Quiz 5", 3, "2026-10-13");
        complete(2);
        list();

        System.out.println("-- Type tests --");
        System.out.println("  addTask(\"Bad\", \"1\", ...)  -> compile-time error (uncomment to see)");
        try {
            addTask("Bad", Integer.parseInt("abc"), "2026-10-20");
        } catch (NumberFormatException e) {
            System.out.println("  parseInt(\"abc\") -> " + e);
        }
        try {
            addTask("Bad", 1, "20-10-2026");
        } catch (Exception e) {
            System.out.println("  bad date -> " + e.getClass().getSimpleName());
        }
        System.out.println("  Integer.MAX_VALUE + 1 = " + (Integer.MAX_VALUE + 1) + " (silent wraparound)");

        System.out.println("-- Benchmark --");
        int n = 200_000;
        long s = System.nanoTime();
        tasks.clear();
        Random r = new Random(42);
        for (int i = 0; i < n; i++) {
            addTask("t" + i, r.nextInt(5), "2026-10-" + (10 + r.nextInt(18)));
        }
        list_quiet();
        System.out.printf("  %d tasks added+sorted in %.1f ms%n", n, (System.nanoTime() - s) / 1e6);
    }

    static void list_quiet() {
        List<Task> sorted = new ArrayList<>(tasks);
        sorted.sort(Comparator.comparingInt(Task::priority).thenComparing(Task::due));
    }
}
