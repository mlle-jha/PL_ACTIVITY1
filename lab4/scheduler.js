const tasks = [];
let taskId = 1;

function addTask(title, priority, dueDate) {
    const task = {
        id: taskId,
        title: title,
        priority: priority,
        dueDate: new Date(dueDate),
        done: false
    };
    tasks.push(task);
    taskId++;
    return task;
}

function completeTask(id) {
    for (const task of tasks) {
        if (task.id === id) {
            task.done = true;
        }
    }
}

function sortTasks() {
    return tasks.slice().sort(function(a, b) {
        if (a.priority !== b.priority) {
            return a.priority - b.priority;
        }
        return a.dueDate - b.dueDate;
    });
}

function showTasks() {
    const sorted = sortTasks();
    for (const task of sorted) {
        let status = "";
        if (task.done) {
            status = "(done)";
        }
        console.log(
            "ID: " + task.id +
            " | Task: " + task.title +
            " | Priority: " + task.priority +
            " | Due: " + task.dueDate.toISOString().slice(0, 10) +
            " | Status: " + status
        );
    }
}

console.log("JavaScript:");

addTask("Write report", 2, "2026-10-15");
addTask("Fix bug", 1, "2026-10-10");
addTask("Email team", 3, "2026-10-12");

completeTask(2);

console.log("\n-- Task List --");
showTasks();

console.log("\n-- Type Tests --");

const badTask = addTask("Bad Task", "1", "2026-10-20");

console.log("Invalid priority was accepted.");

console.log(
    '"1" + 1 =',
    badTask.priority + 1,
    "(string concatenation)"
);

console.log(
    '"1" - 1 =',
    badTask.priority - 1,
    "(converted to a number)"
);

tasks.pop();

console.log(
    "'5' + 3 =",
    "5" + 3
);

console.log(
    "'5' - 3 =",
    "5" - 3
);

console.log(
    "2 ** 53 + 1 =",
    2 ** 53 + 1
);

const badDate = addTask("Bad Date", 1, "not-a-date");

console.log(
    "Invalid date:",
    String(badDate.dueDate)
);

tasks.pop();

console.log("\n-- Benchmark --");

tasks.length = 0;
taskId = 1;

let seed = 42;

function randomNumber(max) {
    seed = (seed * 1103515245 + 12345) & 0x7fffffff;
    return seed % max;
}

const numberOfTasks = 200000;

const startTime = process.hrtime.bigint();

for (let i = 0; i < numberOfTasks; i++) {
    const priority = randomNumber(5);
    const day = 10 + randomNumber(18);
    addTask(
        "Task " + i,
        priority,
        "2026-10-" + day
    );
}

sortTasks();

const endTime = process.hrtime.bigint();

const totalTime = Number(endTime - startTime) / 1000000;

console.log(
    numberOfTasks,
    "tasks added and sorted in",
    totalTime.toFixed(1),
    "ms"
);