import pytest

from core.graph.course_graph import CourseGraph
from core.models.course import Course


def make_course(course_id: str, difficulty: int = 1) -> Course:
    return Course(
        id=course_id,
        title=course_id.title().replace("_", " "),
        description=f"Course {course_id}",
        difficulty=difficulty,
    )


def test_add_course_and_prerequisites_basic():
    graph = CourseGraph()

    ds = make_course("data_structures")
    alg = make_course("algorithms")
    adv = make_course("advanced_programming")

    graph.add_course(ds)
    graph.add_course(alg)
    graph.add_course(adv)

    # ds -> alg -> adv
    graph.add_prerequisite("data_structures", "algorithms")
    graph.add_prerequisite("algorithms", "advanced_programming")

    # Direct prereqs
    assert graph.get_prerequisites("algorithms") == {"data_structures"}
    assert graph.get_prerequisites("advanced_programming") == {"algorithms"}

    # Graph and reverse_graph structure
    assert "algorithms" in graph.graph["data_structures"]
    assert "advanced_programming" in graph.graph["algorithms"]
    assert "data_structures" in graph.reverse_graph["algorithms"]
    assert "algorithms" in graph.reverse_graph["advanced_programming"]


def test_find_all_prerequisites_transitive():
    graph = CourseGraph()

    ds = make_course("data_structures")
    alg = make_course("algorithms")
    adv = make_course("advanced_programming")

    for c in (ds, alg, adv):
        graph.add_course(c)

    # ds -> alg -> adv
    graph.add_prerequisite("data_structures", "algorithms")
    graph.add_prerequisite("algorithms", "advanced_programming")

    all_prereqs_adv = graph.find_all_prerequisites("advanced_programming")
    assert all_prereqs_adv == {"data_structures", "algorithms"}

    all_prereqs_alg = graph.find_all_prerequisites("algorithms")
    assert all_prereqs_alg == {"data_structures"}

    all_prereqs_ds = graph.find_all_prerequisites("data_structures")
    assert all_prereqs_ds == set()


def test_topological_sort_valid_order():
    graph = CourseGraph()

    ds = make_course("data_structures")
    alg = make_course("algorithms")
    adv = make_course("advanced_programming")
    math = make_course("discrete_math")

    for c in (ds, alg, adv, math):
        graph.add_course(c)

    # ds -> alg -> adv
    graph.add_prerequisite("data_structures", "algorithms")
    graph.add_prerequisite("algorithms", "advanced_programming")
    # math is independent

    order = graph.topological_sort()
    # Order must respect dependencies:
    # ds before alg, alg before adv.
    assert order.index("data_structures") < order.index("algorithms")
    assert order.index("algorithms") < order.index("advanced_programming")
    # math can be anywhere, but must be present
    assert "discrete_math" in order
    assert set(order) == {
        "data_structures",
        "algorithms",
        "advanced_programming",
        "discrete_math",
    }


def test_topological_sort_cycle_detection():
    graph = CourseGraph()

    a = make_course("a")
    b = make_course("b")

    graph.add_course(a)
    graph.add_course(b)

    # a -> b and b -> a creates a cycle
    graph.add_prerequisite("a", "b")
    graph.add_prerequisite("b", "a")

    with pytest.raises(ValueError):
        _ = graph.topological_sort()


def test_add_content_appends_not_overwrites():
    graph = CourseGraph()
    ds = make_course("data_structures")
    graph.add_course(ds)

    graph.add_content("data_structures", "Arrays")
    graph.add_content("data_structures", "Linked Lists")
    graph.add_content("data_structures", "Stacks")

    content = graph.get_content("data_structures")
    assert content == ["Arrays", "Linked Lists", "Stacks"]
