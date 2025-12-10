from __future__ import annotations

from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class RecommendationItem:
    """
    Represents a single course recommendation for a student.

    Attributes:
        course_id: The recommended course's ID.
        score: A numeric score representing how strongly this is recommended.
        explanation: A short human-readable explanation of why this was recommended.
    """

    course_id: str
    score: float
    explanation: str
