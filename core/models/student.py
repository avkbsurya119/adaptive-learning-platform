from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Set

from core.history.history import StudentHistory


@dataclass(eq=True)
class Student:
    """
    Represents a student in the system.

    Attributes:
        id: Unique student identifier (e.g., "S101").
        name: Student name.
        age: Age in years.
        gender: Free-form gender string (for simplicity; can be constrained later).
        current_course_id: The course the student is currently focused on.
        completed_sequences: Set of sequence IDs the student has completed.
        progress: Simple integer count of completed sequences.
        history: StudentHistory storing ordered Activity objects.
    """

    id: str
    name: str
    age: int
    gender: str
    current_course_id: Optional[str] = None
    completed_sequences: Set[str] = field(default_factory=set)
    progress: int = 0
    history: StudentHistory = field(default_factory=StudentHistory)

    def update_progress(
        self,
        course_id: str,
        sequence_id: str,
        score: Optional[int] = None,
    ) -> None:
        """
        Mark progress on a given sequence within a course.

        Behavior:
            - If the sequence is newly completed:
                * Add its ID to completed_sequences
                * Increment progress by 1
            - Always logs a 'sequence_completion' activity.
            - If score is provided, also logs a separate 'quiz' activity.

        This mirrors the original design where each completion and quiz
        event was recorded separately.
        """
        is_new_completion = sequence_id not in self.completed_sequences
        if is_new_completion:
            self.completed_sequences.add(sequence_id)
            self.progress += 1

        # Log sequence completion
        self.history.append_activity(
            activity_type="sequence_completion",
            score=score,
            metadata={"course_id": course_id, "sequence_id": sequence_id},
        )

        # Log quiz result, if provided
        if score is not None:
            self.history.append_activity(
                activity_type="quiz",
                score=score,
                metadata={"course_id": course_id, "sequence_id": sequence_id},
            )

    def change_current_course(self, course_id: Optional[str]) -> None:
        """Set or clear the current course for this student."""
        self.current_course_id = course_id
