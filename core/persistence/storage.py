from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

from core.models.student import Student
from core.models.course import Course
from core.models.sequence import Sequence


# ---------------------------------------------------------------
# Helper: Convert Student to dict
# ---------------------------------------------------------------


def student_to_dict(student: Student) -> dict:
    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "gender": student.gender,
        "current_course_id": student.current_course_id,
        "completed_sequences": list(student.completed_sequences),
        "progress": student.progress,
        "history": [
            {
                "activity_type": a.activity_type,
                "timestamp": a.timestamp.isoformat(),
                "score": a.score,
                "metadata": a.metadata,
            }
            for a in student.history.to_list()
        ],
    }


def student_from_dict(data: dict) -> Student:
    student = Student(
        id=data["id"],
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
    )
    student.current_course_id = data["current_course_id"]
    student.completed_sequences = set(data["completed_sequences"])
    student.progress = data["progress"]

    # Rebuild activity history
    for a in data["history"]:
        timestamp = datetime.fromisoformat(a["timestamp"])
        student.history.append_activity(
            activity_type=a["activity_type"],
            score=a["score"],
            metadata=a["metadata"],
            timestamp=timestamp,
        )
    return student


# ---------------------------------------------------------------
# Helper: Convert Course to dict
# ---------------------------------------------------------------


def course_to_dict(course: Course) -> dict:
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "difficulty": course.difficulty,
        "sequences": [
            {
                "id": seq.id,
                "title": seq.title,
                "duration_hours": seq.duration.total_seconds() / 3600.0,
                "order": seq.order,
            }
            for seq in course.sequences
        ],
    }


def course_from_dict(data: dict) -> Course:
    c = Course(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        difficulty=data["difficulty"],
    )
    for seq in data["sequences"]:
        c.add_sequence(
            Sequence(
                id=seq["id"],
                title=seq["title"],
                duration=timedelta(hours=seq["duration_hours"]),
                order=seq["order"],
            )
        )
    return c


# ---------------------------------------------------------------
# Persistence API
# ---------------------------------------------------------------


def save_students(path: str, students: Dict[str, Student]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {sid: student_to_dict(stu) for sid, stu in students.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_students(path: str) -> Dict[str, Student]:
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    return {sid: student_from_dict(data) for sid, data in payload.items()}


def save_courses(path: str, courses: Dict[str, Course]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {cid: course_to_dict(c) for cid, c in courses.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_courses(path: str) -> Dict[str, Course]:
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    return {cid: course_from_dict(data) for cid, data in payload.items()}


# ---------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------


def seed_example_data() -> Dict[str, Course]:
    """Creates a small course dictionary for demos."""
    c1 = Course(
        id="data_structures",
        title="Data Structures",
        description="Intro to DS",
        difficulty=2,
    )
    c1.add_sequence(Sequence("ds_arrays", "Arrays", timedelta(hours=1), 1))
    c1.add_sequence(Sequence("ds_ll", "Linked Lists", timedelta(hours=1.5), 2))

    c2 = Course(
        id="algorithms",
        title="Algorithms",
        description="Intro to Algo",
        difficulty=3,
    )
    c2.add_sequence(Sequence("alg_sort", "Sorting", timedelta(hours=2), 1))

    return {"data_structures": c1, "algorithms": c2}


def clear_data(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
