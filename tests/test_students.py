from core.models.student import Student
from core.history.history import StudentHistory


def test_student_update_progress_increments_once_per_sequence():
    student = Student(id="S101", name="Alice", age=20, gender="Female")

    # First completion of seq1
    student.update_progress(course_id="data_structures", sequence_id="seq1", score=85)
    assert student.progress == 1
    assert "seq1" in student.completed_sequences

    # Calling again with same sequence should NOT increment progress
    student.update_progress(course_id="data_structures", sequence_id="seq1", score=90)
    assert student.progress == 1  # unchanged
    assert "seq1" in student.completed_sequences

    # But history should have 4 activities:
    # 2 for first call (completion + quiz), 2 for second call
    activities = list(student.history)
    assert len(activities) == 4
    types = [a.activity_type for a in activities]
    assert types.count("sequence_completion") == 2
    assert types.count("quiz") == 2


def test_student_change_current_course_and_history_logging():
    student = Student(id="S102", name="Bob", age=22, gender="Male")
    assert student.current_course_id is None

    student.change_current_course("algorithms")
    assert student.current_course_id == "algorithms"

    # Complete two different sequences
    student.update_progress("algorithms", "seq1", score=70)
    student.update_progress("algorithms", "seq2", score=95)

    assert student.progress == 2
    assert student.completed_sequences == {"seq1", "seq2"}

    activities = list(student.history)
    # 2 calls, each logs completion + quiz => 4 activities
    assert len(activities) == 4

    # Ensure metadata is consistent
    for a in activities:
        assert a.metadata is not None
        assert a.metadata["course_id"] == "algorithms"
        assert a.metadata["sequence_id"] in {"seq1", "seq2"}
