from datetime import timedelta

from core.graph.course_graph import CourseGraph
from core.models.course import Course
from core.models.sequence import Sequence
from core.models.student import Student
from core.recommendations.recommendation_engine import RecommendationEngine
from core.scheduling.sequence_scheduler import SequenceScheduler, SequenceTask
from core.search.trie import ContentTrie


def test_end_to_end_learning_flow():
    # Setup course + sequences
    course = Course(
        id="data_structures",
        title="Data Structures",
        description="Intro DS",
        difficulty=2,
    )
    seq1 = Sequence("ds_arrays", "Arrays", timedelta(hours=1), 1)
    seq2 = Sequence("ds_ll", "Linked Lists", timedelta(hours=1), 2)
    course.add_sequence(seq1)
    course.add_sequence(seq2)

    # Graph
    graph = CourseGraph()
    graph.add_course(course)

    # Trie
    trie = ContentTrie()
    trie.insert(course.title, course.title)
    for s in course.sequences:
        trie.insert(s.title, f"{course.title} - {s.title}")

    # Scheduler
    scheduler = SequenceScheduler()
    for s in course.sequences:
        scheduler.schedule(
            SequenceTask(
                priority=course.difficulty,
                course_id=course.id,
                sequence_id=s.id,
                duration=s.duration,
            )
        )

    # Student
    student = Student(id="S1", name="Alice", age=20, gender="F")
    student.change_current_course(course.id)

    # Student completes all scheduled sequences
    while not scheduler.is_empty():
        task = scheduler.dequeue_next()
        score = len(task.sequence_id) * 10
        student.update_progress(
            course_id=task.course_id,
            sequence_id=task.sequence_id,
            score=score,
        )

    # Ensure progress reflects both sequences
    assert student.progress == 2
    assert student.completed_sequences == {"ds_arrays", "ds_ll"}

    # Search check
    results = trie.autocomplete("Arr")
    assert any("Arrays" in r for r in results)

    # Recommendation engine on a small course dict
    engine = RecommendationEngine()
    recs = engine.recommend_for(student, {"data_structures": course}, top_n=1)
    assert len(recs) == 1
    assert recs[0].course_id == "data_structures"
    # Score should be deterministic and positive
    assert recs[0].score > 0
