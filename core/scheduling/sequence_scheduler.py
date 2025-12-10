from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import List, Optional
import heapq
import itertools


@dataclass(order=True)
class SequenceTask:
    """
    Represents a scheduled learning sequence.

    Ordering:
        Tasks are ordered by (priority, _order) where:
        - priority: lower number means higher priority (1 > 5)
        - _order : insertion order to ensure FIFO for same priority.
    """

    priority: int
    _order: int = field(init=False, repr=False, compare=True)
    course_id: str = field(compare=False)
    sequence_id: str = field(compare=False)
    duration: timedelta = field(compare=False)

    def __post_init__(self) -> None:
        # _order will be filled in by the scheduler when scheduling.
        # We initialize with 0 to satisfy dataclass, but it is overwritten.
        object.__setattr__(self, "_order", 0)


class SequenceScheduler:
    """
    Priority-based scheduler for course sequences.

    - Lower priority number => higher priority (1 runs before 5).
    - Among the same priority, tasks are served in FIFO order.
    - Internally uses a min-heap (heapq) with a global counter.
    """

    def __init__(self) -> None:
        self._heap: List[SequenceTask] = []
        self._counter = itertools.count()  # ensures stable ordering

    def schedule(self, task: SequenceTask) -> None:
        """
        Schedule a new sequence task.

        The task's internal _order is set automatically to preserve
        the insertion order among tasks with the same priority.
        """
        order_value = next(self._counter)
        # Create a new task with same data but updated _order
        object.__setattr__(task, "_order", order_value)
        heapq.heappush(self._heap, task)

    def dequeue_next(self) -> Optional[SequenceTask]:
        """
        Return and remove the next scheduled task.

        Returns:
            The highest-priority task, or None if the scheduler is empty.
        """
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def is_empty(self) -> bool:
        """Return True if no tasks are scheduled."""
        return not self._heap

    def dequeue_by_course(self, course_id: str) -> List[SequenceTask]:
        """
        Remove and return all tasks for a given course_id.

        Returns:
            A list of tasks that belonged to the course.
        """
        remaining: List[SequenceTask] = []
        removed: List[SequenceTask] = []

        while self._heap:
            task = heapq.heappop(self._heap)
            if task.course_id == course_id:
                removed.append(task)
            else:
                remaining.append(task)

        # Rebuild heap with remaining tasks
        for task in remaining:
            heapq.heappush(self._heap, task)

        return removed

    def update_priority(self, course_id: str, new_priority: int) -> None:
        """
        Update the priority of all tasks belonging to a course.

        This is implemented by:
            - Popping all tasks
            - Adjusting those matching course_id
            - Rebuilding the heap

        Lower numbers mean higher priority.
        """
        updated_tasks: List[SequenceTask] = []
        while self._heap:
            task = heapq.heappop(self._heap)
            if task.course_id == course_id:
                # Create a new task with updated priority but same identity
                updated_task = SequenceTask(
                    priority=new_priority,
                    course_id=task.course_id,
                    sequence_id=task.sequence_id,
                    duration=task.duration,
                )
                updated_tasks.append(updated_task)
            else:
                updated_tasks.append(task)

        # Reset heap and counter (to keep ordering deterministic from now on)
        self._heap.clear()
        self._counter = itertools.count()
        for task in updated_tasks:
            self.schedule(task)

    def list_scheduled(self) -> List[SequenceTask]:
        """
        Return a snapshot list of scheduled tasks in the order
        they would be dequeued (without mutating the scheduler).
        """
        copied_heap = list(self._heap)
        heapq.heapify(copied_heap)
        ordered: List[SequenceTask] = []
        while copied_heap:
            ordered.append(heapq.heappop(copied_heap))
        return ordered
