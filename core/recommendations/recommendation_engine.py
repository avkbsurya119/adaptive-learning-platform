# core/recommendations/recommendation_engine.py
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from core.models.course import Course
from core.models.student import Student
from core.models.recommendation import RecommendationItem


class RecommendationEngine:
    """
    Deterministic recommendation engine for courses.

    Scoring factors:
        - progress gap
        - difficulty match
        - recency

    This engine does NOT modify student or course objects.
    """

    def __init__(
        self,
        weight_progress_gap: float = 0.5,
        weight_difficulty: float = 0.3,
        weight_recency: float = 0.2,
    ) -> None:
        self.weight_progress_gap = weight_progress_gap
        self.weight_difficulty = weight_difficulty
        self.weight_recency = weight_recency

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

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

        avg_difficulty = self._compute_average_difficulty(student, courses)
        last_activity_time = self._compute_last_activity_time(student)

        for course_id, course in courses.items():
            score, explanation = self._score_course(
                student=student,
                course=course,
                avg_difficulty=avg_difficulty,
                last_activity_time=last_activity_time,
            )

            scored.append(
                RecommendationItem(
                    course_id=course_id,
                    score=score,
                    explanation=explanation,
                )
            )

        # Sort descending by score
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_n]

    # ------------------------------------------------------------------ #
    # Scoring helpers
    # ------------------------------------------------------------------ #

    def _score_course(
        self,
        student: Student,
        course: Course,
        avg_difficulty: float,
        last_activity_time: Optional[datetime],
    ) -> (float, str):
        """
        Compute weighted score and human-readable explanation for a course.
        """
        # 1) Progress gap: more remaining content → higher gap → more to learn
        total_sequences = len(course.sequences)
        completed_for_course = 0
        for seq in course.sequences:
            if seq.id in student.completed_sequences:
                completed_for_course += 1

        if total_sequences > 0:
            progress_gap = float(total_sequences - completed_for_course) / float(
                total_sequences
            )
        else:
            # Edge case: course has no sequences; treat as fully recommendable
            progress_gap = 1.0

        # 2) Difficulty match: closer to student's average difficulty is better
        difficulty_difference = abs(course.difficulty - avg_difficulty)
        # Normalise over a reasonable range (0–5)
        difficulty_score = 1.0 - (difficulty_difference / 5.0)
        if difficulty_score < 0.0:
            difficulty_score = 0.0

        # 3) Recency: more recent global activity → mild boost
        recency_score = 0.0
        if last_activity_time is not None:
            days_since_last = (datetime.now() - last_activity_time).days
            # Simple linear decay up to 30 days
            recency_score = 1.0 - (float(days_since_last) / 30.0)
            if recency_score < 0.0:
                recency_score = 0.0

        score = (
            self.weight_progress_gap * progress_gap
            + self.weight_difficulty * difficulty_score
            + self.weight_recency * recency_score
        )

        explanation = (
            "Progress gap={:.2f}, Difficulty match={:.2f}, Recency={:.2f}".format(
                progress_gap, difficulty_score, recency_score
            )
        )

        return score, explanation

    def _compute_average_difficulty(
        self,
        student: Student,
        courses: Dict[str, Course],
    ) -> float:
        """
        Compute average difficulty of courses for which the student
        has completed at least one sequence.
        """
        difficulties = []

        for course in courses.values():
            for seq in course.sequences:
                if seq.id in student.completed_sequences:
                    difficulties.append(course.difficulty)
                    break  # only count each course once

        if not difficulties:
            # Neutral baseline if student has no past activity
            return 2.5

        return float(sum(difficulties)) / float(len(difficulties))

    def _compute_last_activity_time(self, student: Student) -> Optional[datetime]:
        """
        Return timestamp of the most recent activity in student's history, or None.
        """
        if len(student.history) == 0:
            return None

        times = [activity.timestamp for activity in student.history]
        return max(times)
