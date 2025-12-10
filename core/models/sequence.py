from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass(eq=True, frozen=True)
class Sequence:
    """
    Represents a learning sequence (module/lesson) inside a course.

    Attributes:
        id: Unique identifier for this sequence (e.g., "ds_arrays_basics").
        title: Human-readable title.
        duration: Approximate duration for completion.
        order: Position within the course (lower means earlier in the course).
    """

    id: str
    title: str
    duration: timedelta
    order: int

    def key(self) -> str:
        """
        A stable key that can be used for indexing, completion tracking, etc.
        By default this is just the sequence id.
        """
        return self.id
