from datetime import timedelta

class SequenceQueue:
    def __init__(self, size=20):
        self.tasks = [None] * size  # Each task is a tuple: (course_name, priority, duration)
        self.front = 0
        self.rear = -1
        self.size = size
        self.count = 0

    def enqueue(self, task):
        if self.count == self.size:
            raise Exception("Queue is full")
        self.rear = (self.rear + 1) % self.size
        self.tasks[self.rear] = task
        self.count += 1
    
    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        task = self.tasks[self.front]
        self.tasks[self.front] = None
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return task
    
    def is_empty(self):
        return self.count == 0

    def display(self):
        if self.is_empty():
            print("Queue is empty")
            return 
        print("Current tasks in the queue:")
        for i in range(self.count):
            index = (self.front + i) % self.size
            print(self.tasks[index])

    def schedule_course(self, course_name, duration, priority):
        """Schedule a course by enqueuing it with a specified duration and priority."""
        task = (course_name, priority, duration)
        self.enqueue(task)
        print(f"Successfully scheduled course: {course_name} with duration {duration} and priority {priority}.")

    def update_priority(self, course_name, new_priority):
        """Update the priority of a course in the queue."""
        # Remove all tasks, update the priority of the specific course, and re-insert.
        tasks = []
        found = False

        # Dequeue all tasks
        while not self.is_empty():
            task = self.dequeue()
            if task[0] == course_name:
                # Update the priority for the specified course
                tasks.append((course_name, new_priority, task[2]))
                found = True
            else:
                tasks.append(task)

        if not found:
            # If course not found, add it as a new task with the given priority
            print(f"Course {course_name} not found; adding it with priority {new_priority}.")
            tasks.append((course_name, new_priority, timedelta(days=1)))  # Default 1 day duration for new additions

        # Sort by priority (lower number = higher priority) and re-enqueue
        tasks.sort(key=lambda x: x[1])  # Priority is now reliably an integer

        for task in tasks:
            self.enqueue(task)

        print(f"Updated priority for course: {course_name} to {new_priority}")