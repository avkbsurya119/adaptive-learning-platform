from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .sequence import Sequence


@dataclass(eq=True)
class Course:
    """
    Represents a course in the learning platform.

    Attributes:
        id: Unique course identifier (e.g., "data_structures").
        title: Human-readable name.
        description: Short description of the course.
        difficulty: Integer difficulty level (e.g., 1–5).
        sequences: Ordered list of learning sequences in this course.
    """

    id: str
    title: str
    description: str
    difficulty: int = 1
    sequences: List[Sequence] = field(default_factory=list)

    def add_sequence(self, sequence: Sequence) -> None:
        """Add a sequence to the course and keep sequences ordered by 'order'."""
        self.sequences.append(sequence)
        self.sequences.sort(key=lambda seq: seq.order)

    def get_sequence_ids(self) -> List[str]:
        """Return the sequence IDs in the order they should be completed."""
        return [seq.id for seq in self.sequences]

    def get_sequence_by_id(self, sequence_id: str) -> Optional[Sequence]:
        """Return a sequence by its ID, or None if not found."""
        for seq in self.sequences:
            if seq.id == sequence_id:
                return seq
        return None
