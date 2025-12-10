from __future__ import annotations

from typing import Dict, Optional

from core.models.student import Student
from core.persistence.storage import load_students, save_students


class StudentService:
    """Service layer for managing Student entities.

    This abstracts:
    - In-memory storage (dict)
    - Optional persistence to JSON using core.persistence.storage
    """

    def __init__(self, storage_path: str | None = None) -> None:
        self._storage_path = storage_path
        self._students: Dict[str, Student] = {}

        if storage_path is not None:
            try:
                self._students = load_students(storage_path)
            except Exception:
                # For demo use-cases we fail gracefully and start empty
                self._students = {}

    @property
    def students(self) -> Dict[str, Student]:
        """Read-only view of all students."""
        return self._students

    def add_student(self, student: Student) -> None:
        """Register or overwrite a student."""
        self._students[student.id] = student

    def get_student(self, student_id: str) -> Optional[Student]:
        """Fetch a student by id, or None if missing."""
        return self._students.get(student_id)

    def exists(self, student_id: str) -> bool:
        """Check if a student with the given id exists."""
        return student_id in self._students

    def remove_student(self, student_id: str) -> None:
        """Remove a student if present."""
        self._students.pop(student_id, None)

    def save(self) -> None:
        """Persist all students to configured storage, if enabled."""
        if self._storage_path is not None:
            save_students(self._storage_path, self._students)
