"""Optional service layer for managing student operations.

This is a placeholder for future expansion. The current CLI calls
core.models.student directly, but this module allows a cleaner abstraction
if expanding into FastAPI or a web backend.
"""

from typing import Dict
from core.models.student import Student


class StudentService:
    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        self.students[student.id] = student

    def get_student(self, student_id: str) -> Student | None:
        return self.students.get(student_id)
