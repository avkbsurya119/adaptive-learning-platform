# tests/test_recommendation_engine.py
from datetime import timedelta, datetime

from core.recommendations.recommendation_engine import RecommendationEngine
from core.models.course import Course
from core.models.sequence import Sequence
from core.models.student import Student


def make_course(cid: str, diff: int, seq_ids: list[str]) -> Course:
    course = Course(
        id=cid,
        title=cid.title(),
        description="test",
        difficulty=diff,
    )
    for i, sid in enumerate(seq_ids, start=1):
        course.add_sequence(
            Sequence(
                id=sid,
                title=sid.title(),
                duration=timedelta(hours=1),
                order=i,
            )
        )
    return course


def test_recommendations_sorted_and_scored():
    engine = RecommendationEngine(
        weight_progress_gap=0.5,
        weight_difficulty=0.3,
        weight_recency=0.2,
    )

    # Student with no activity yet
    student = Student(id="S1", name="Test", age=20, gender="M")

    # Define courses
    c1 = make_course("data_structures", diff=2, seq_ids=["a", "b"])
    c2 = make_course("algorithms", diff=3, seq_ids=["c", "d", "e"])
    c3 = make_course("ml", diff=5, seq_ids=["x"])

    courses = {
        "data_structures": c1,
        "algorithms": c2,
        "ml": c3,
    }

    recs = engine.recommend_for(student, courses, top_n=3)
    assert len(recs) == 3
    # Score must be descending
    assert recs[0].score >= recs[1].score >= recs[2].score


def test_progress_gap_affects_score():
    engine = RecommendationEngine()

    student = Student(id="S1", name="A", age=20, gender="F")

    c = Course(id="test", title="Test", description="d", difficulty=2)
    c.add_sequence(
        Sequence(id="s1", title="Seq1", duration=timedelta(hours=1), order=1)
    )
    c.add_sequence(
        Sequence(id="s2", title="Seq2", duration=timedelta(hours=1), order=2)
    )

    # Student completes 1 of 2 sequences
    student.completed_sequences.add("s1")

    recs = engine.recommend_for(student, {"test": c})
    assert len(recs) == 1
    item = recs[0]
    assert "Progress gap" in item.explanation
    assert item.score > 0  # should have some positive value


def test_recency_affects_score():
    engine = RecommendationEngine()

    student = Student(id="S1", name="A", age=20, gender="F")

    # Fake recent activity (1 day ago)
    student.history.append_activity(
        activity_type="sequence_completion",
        timestamp=datetime.now() - timedelta(days=1),
        metadata={"course_id": "x", "sequence_id": "y"},
    )

    c = Course(id="temp", title="T", description="d", difficulty=2)
    rec = engine.recommend_for(student, {"temp": c})[0]

    assert "Recency" in rec.explanation
    assert rec.score > 0
