from __future__ import annotations

from array import array
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional

from core.models.activity import Activity


class StudentHistory:
    """
    Array-based history of student activities.

    Internally uses:
        - _index: array('I') storing integer indices
        - _activities: list[Activity]

    This mirrors the idea of your original StudentHistoryArray ADT,
    while providing a clean Pythonic interface.
    """

    def __init__(self) -> None:
        # Index positions into _activities
        self._index: array = array("I")
        # Actual activity objects
        self._activities: List[Activity] = []

    def append_activity(
        self,
        activity_type: str,
        score: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Append a new Activity to the history.

        Args:
            activity_type: Logical type of the activity (e.g., "sequence_completion", "quiz").
            score: Optional score associated with the activity.
            metadata: Optional dictionary with extra info.
            timestamp: Optional explicit timestamp; if None, uses datetime.now().
        """
        if timestamp is None:
            timestamp = datetime.now()

        activity = Activity(
            activity_type=activity_type,
            timestamp=timestamp,
            score=score,
            metadata=metadata,
        )

        self._index.append(len(self._activities))
        self._activities.append(activity)

    def iterate_activities(self) -> Iterator[Activity]:
        """Yield activities in the order they were appended."""
        for idx in self._index:
            yield self._activities[idx]

    def __iter__(self) -> Iterator[Activity]:
        return self.iterate_activities()

    def __len__(self) -> int:
        return len(self._index)

    def to_list(self) -> List[Activity]:
        """Return a list copy of all activities in order."""
        return list(self.iterate_activities())
