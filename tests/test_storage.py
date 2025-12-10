import os
from datetime import timedelta, datetime

from core.persistence.storage import (
    save_students,
    load_students,
    save_courses,
    load_courses,
)
from core.models.student import Student
from core.models.course import Course
from core.models.sequence import Sequence


def test_save_and_load_students(tmp_path):
    p = tmp_path / "students.json"

    # Create a student
    s = Student(id="S1", name="Alice", age=20, gender="F")
    s.update_progress("data_structures", "seq1", score=85)

    students = {"S1": s}

    save_students(str(p), students)
    loaded = load_students(str(p))

    assert "S1" in loaded
    assert loaded["S1"].name == "Alice"
    assert loaded["S1"].progress == 1
    assert len(loaded["S1"].history.to_list()) == 2  # completion + quiz


def test_save_and_load_courses(tmp_path):
    p = tmp_path / "courses.json"

    c = Course(
        id="test",
        title="Test",
        description="d",
        difficulty=3,
    )
    c.add_sequence(Sequence("s1", "Seq1", timedelta(hours=1), 1))
    c.add_sequence(Sequence("s2", "Seq2", timedelta(hours=2), 2))

    save_courses(str(p), {"test": c})
    loaded = load_courses(str(p))

    assert "test" in loaded
    lc = loaded["test"]

    assert lc.title == "Test"
    assert len(lc.sequences) == 2
    assert lc.sequences[1].duration.total_seconds() == 7200
