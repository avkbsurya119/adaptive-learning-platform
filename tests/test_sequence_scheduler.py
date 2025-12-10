from datetime import timedelta

from core.scheduling.sequence_scheduler import SequenceScheduler, SequenceTask


def make_task(
    course_id: str,
    sequence_id: str,
    priority: int,
    hours: int = 1,
) -> SequenceTask:
    return SequenceTask(
        priority=priority,
        course_id=course_id,
        sequence_id=sequence_id,
        duration=timedelta(hours=hours),
    )


def test_fifo_with_same_priority():
    scheduler = SequenceScheduler()

    t1 = make_task("data_structures", "seq1", priority=2)
    t2 = make_task("data_structures", "seq2", priority=2)
    t3 = make_task("algorithms", "seq1", priority=2)

    scheduler.schedule(t1)
    scheduler.schedule(t2)
    scheduler.schedule(t3)

    # Same priority => should come out in insertion order
    order = [
        scheduler.dequeue_next(),
        scheduler.dequeue_next(),
        scheduler.dequeue_next(),
    ]
    ids = [(t.course_id, t.sequence_id) for t in order]

    assert ids == [
        ("data_structures", "seq1"),
        ("data_structures", "seq2"),
        ("algorithms", "seq1"),
    ]


def test_lower_priority_number_runs_first():
    scheduler = SequenceScheduler()

    high = make_task("advanced_programming", "seq1", priority=3)  # lower priority
    low = make_task("data_structures", "seq1", priority=1)  # higher priority

    scheduler.schedule(high)
    scheduler.schedule(low)

    first = scheduler.dequeue_next()
    second = scheduler.dequeue_next()

    assert (first.course_id, first.sequence_id) == ("data_structures", "seq1")
    assert (second.course_id, second.sequence_id) == ("advanced_programming", "seq1")


def test_dequeue_next_returns_none_when_empty():
    scheduler = SequenceScheduler()
    assert scheduler.dequeue_next() is None
    assert scheduler.is_empty() is True


def test_dequeue_by_course_removes_only_that_course():
    scheduler = SequenceScheduler()

    t1 = make_task("data_structures", "seq1", priority=1)
    t2 = make_task("data_structures", "seq2", priority=2)
    t3 = make_task("algorithms", "seq1", priority=1)

    scheduler.schedule(t1)
    scheduler.schedule(t2)
    scheduler.schedule(t3)

    removed = scheduler.dequeue_by_course("data_structures")
    removed_ids = {(t.course_id, t.sequence_id) for t in removed}
    assert removed_ids == {
        ("data_structures", "seq1"),
        ("data_structures", "seq2"),
    }

    # Only algorithms task should remain
    remaining = scheduler.list_scheduled()
    assert len(remaining) == 1
    assert (remaining[0].course_id, remaining[0].sequence_id) == ("algorithms", "seq1")


def test_update_priority_changes_order():
    scheduler = SequenceScheduler()

    # Initially, algorithms has higher numerical priority => runs later
    ds_task = make_task("data_structures", "seq1", priority=1)
    alg_task = make_task("algorithms", "seq1", priority=5)

    scheduler.schedule(ds_task)
    scheduler.schedule(alg_task)

    # Now promote algorithms to highest priority (0)
    scheduler.update_priority("algorithms", new_priority=0)

    # algorithms should now be dequeued first
    first = scheduler.dequeue_next()
    second = scheduler.dequeue_next()

    assert (first.course_id, first.sequence_id) == ("algorithms", "seq1")
    assert (second.course_id, second.sequence_id) == ("data_structures", "seq1")
