from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(eq=True)
class Activity:
    """
    Represents a single activity performed by a student.

    Examples of activity_type:
    - "sequence_completion"
    - "quiz"
    - "course_enrollment"
    - "recommendation_viewed"
    """

    activity_type: str
    timestamp: datetime
    score: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

    def describe(self) -> str:
        """Return a short human-readable description of the activity."""
        base = f"[{self.timestamp.isoformat(timespec='seconds')}] {self.activity_type}"
        if self.score is not None:
            base += f" | score={self.score}"
        if self.metadata:
            base += f" | meta={self.metadata}"
        return base
