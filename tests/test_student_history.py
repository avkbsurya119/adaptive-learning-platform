from core.history.history import StudentHistory


def test_append_and_iterate_history_order():
    history = StudentHistory()

    history.append_activity(
        activity_type="sequence_completion",
        score=80,
        metadata={"course_id": "data_structures", "sequence_id": "seq1"},
    )
    history.append_activity(
        activity_type="quiz",
        score=90,
        metadata={"course_id": "data_structures", "sequence_id": "seq1"},
    )

    activities = list(history.iterate_activities())
    assert len(activities) == 2

    assert activities[0].activity_type == "sequence_completion"
    assert activities[0].score == 80
    assert activities[0].metadata["sequence_id"] == "seq1"

    assert activities[1].activity_type == "quiz"
    assert activities[1].score == 90
    assert activities[1].metadata["sequence_id"] == "seq1"


def test_history_len_matches_number_of_activities():
    history = StudentHistory()
    assert len(history) == 0

    history.append_activity("sequence_completion")
    history.append_activity("quiz", score=75)

    assert len(history) == 2
    assert len(history.to_list()) == 2
