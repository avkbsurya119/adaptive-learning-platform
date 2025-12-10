from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import exp
from typing import Dict, List

from core.models.course import Course
from core.models.student import Student
from core.models.recommendation import RecommendationItem


@dataclass
class RecommendationEngine:
    """
    Deterministic recommendation engine for courses.

    Scoring factors:
        - progress gap
        - difficulty match
        - recency

    This engine does NOT modify student or course objects.
    """

    # Tunable weights
    weight_progress_gap: float = 0.5
    weight_difficulty: float = 0.3
    weight_recency: float = 0.2

    def recommend_for(
        self,
        student: Student,
        courses: Dict[str, Course],
        top_n: int = 5,
    ) -> List[RecommendationItem]:
        """
        Compute top-N recommended courses for the student.

        Args:
            student: Student object with history.
            courses: Dict mapping course_id -> Course.
            top_n: Number of recommendations to return.

        Returns:
            List[RecommendationItem] sorted by score descending.
        """
        scored: List[RecommendationItem] = []

        # Precompute student stats
        avg_difficulty = self._compute_average_difficulty(student, courses)
        last_activity_time = self._compute_last_activity_time(student)

        for course_id, course in courses.items():
            score, explanation = self._score_course(
                student,
                course,
                avg_difficulty,
                last_activity_time,
            )

            scored.append(
                RecommendationItem(
                    course_id=course_id,
                    score=score,
                    explanation=explanation,
                )
            )

        # Sort by score descending
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_n]

    # ------------------------------------------------------------------ #
    # Scoring helpers
    # ------------------------------------------------------------------ #

    def _score_course(
        self,
        student: Student,
        course: Course,
        avg_difficulty: float,
        last_activity_time: datetime | None,
    ) -> tuple[float, str]:
        """
        Compute weighted score and return (score, explanation).
        """
        # Factor 1: progress gap
        total = len(course.sequences)
        completed = sum(
            1 for seq in course.sequences if seq.id in student.completed_sequences
        )
        if total > 0:
            progress_gap = (total - completed) / total
        else:
            progress_gap = 1  # treat empty course as fully recommendable

        # Factor 2: difficulty match
        difficulty_score = 1 - abs(course.difficulty - avg_difficulty) / 5

        # Factor 3: recency
        recency_score = 0.0
        if last_activity_time is not None:
            days = (datetime.now() - last_activity_time).days
            recency_score = max(0, 1 - days / 30)

        # Weighted sum
        score = (
            self.weight_progress_gap * progress_gap
            + self.weight_difficulty * difficulty_score
            + self.weight_recency * recency_score
        )

        explanation = (
            f"Progress gap={progress_gap:.2f}, "
            f"Difficulty match={difficulty_score:.2f}, "
            f"Recency={recency_score:.2f}"
        )

        return score, explanation

    def _compute_average_difficulty(
        self,
        student: Student,
        courses: Dict[str, Course],
    ) -> float:
        """
        Compute average difficulty of completed sequences.
        Used to determine 'difficulty match'.
        """
        difficulties = []

        for course in courses.values():
            for seq in course.sequences:
                if seq.id in student.completed_sequences:
                    difficulties.append(course.difficulty)

        if not difficulties:
            return 2.5  # neutral baseline

        return sum(difficulties) / len(difficulties)

    def _compute_last_activity_time(self, student: Student):
        """
        Return the timestamp of the most recent activity, or None.
        """
        if len(student.history) == 0:
            return None

        times = [a.timestamp for a in student.history]
        return max(times)
