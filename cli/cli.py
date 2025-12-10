from __future__ import annotations

from typing import Dict, Optional

from core.graph.course_graph import CourseGraph
from core.models.course import Course
from core.models.student import Student
from core.recommendations.recommendation_engine import RecommendationEngine
from core.scheduling.sequence_scheduler import SequenceScheduler, SequenceTask
from core.search.trie import ContentTrie
from core.persistence.storage import seed_example_data, save_students, load_students


STUDENT_STORAGE_PATH = "data/students.json"


class LearningPlatformCLI:
    """
    Minimal interactive CLI that demonstrates the core flows:

    - Load seed courses
    - Build CourseGraph and Trie
    - Register students
    - Search content
    - Enroll in courses
    - Complete sequences (using the scheduler)
    - View history
    - Get recommendations
    """

    def __init__(self) -> None:
        # Core components
        self.course_graph = CourseGraph()
        self.trie = ContentTrie()
        self.scheduler = SequenceScheduler()
        self.recommendation_engine = RecommendationEngine()

        # In-memory student registry
        self.students: Dict[str, Student] = {}

        # Load initial data
        self.courses: Dict[str, Course] = seed_example_data()
        self._init_courses()
        self._load_students()

    # ------------------------------------------------------------------ #
    # Initialization helpers
    # ------------------------------------------------------------------ #

    def _init_courses(self) -> None:
        """Register courses in graph, fill Trie and schedule all sequences."""
        # Example prerequisites mapping:
        # data_structures -> algorithms
        if "data_structures" in self.courses and "algorithms" in self.courses:
            prereq_map = [("data_structures", "algorithms")]
        else:
            prereq_map = []

        for course in self.courses.values():
            self.course_graph.add_course(course)

            # Add course title and sequences to Trie
            self.trie.insert(course.title, course.title)
            for seq in course.sequences:
                self.trie.insert(seq.title, f"{course.title} - {seq.title}")

            # Schedule all sequences with priority based on difficulty
            for seq in course.sequences:
                task = SequenceTask(
                    priority=course.difficulty,  # lower difficulty => higher priority
                    course_id=course.id,
                    sequence_id=seq.id,
                    duration=seq.duration,
                )
                self.scheduler.schedule(task)

        # Add prerequisites to CourseGraph
        for prereq, course_id in prereq_map:
            if prereq in self.courses and course_id in self.courses:
                self.course_graph.add_prerequisite(prereq, course_id)

    def _load_students(self) -> None:
        """Load students from JSON storage if available."""
        try:
            self.students = load_students(STUDENT_STORAGE_PATH)
        except Exception:
            # For demo purposes, ignore load failures
            self.students = {}

    def _save_students(self) -> None:
        """Persist students to JSON storage."""
        save_students(STUDENT_STORAGE_PATH, self.students)

    # ------------------------------------------------------------------ #
    # CLI Loop
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        """Run the main menu loop."""
        while True:
            print("\n=== Adaptive Learning Platform CLI ===")
            print("1. Register student")
            print("2. List courses")
            print("3. Search content")
            print("4. Enroll student in course")
            print("5. Complete next scheduled sequence for student")
            print("6. View student history")
            print("7. Get course recommendations for student")
            print("8. Save & Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self._register_student()
            elif choice == "2":
                self._list_courses()
            elif choice == "3":
                self._search_content()
            elif choice == "4":
                self._enroll_student()
            elif choice == "5":
                self._complete_next_sequence()
            elif choice == "6":
                self._view_student_history()
            elif choice == "7":
                self._show_recommendations()
            elif choice == "8":
                self._save_students()
                print("Data saved. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    # ------------------------------------------------------------------ #
    # Menu operations
    # ------------------------------------------------------------------ #

    def _register_student(self) -> None:
        student_id = input("Enter new student ID: ").strip()
        if not student_id:
            print("Student ID cannot be empty.")
            return

        if student_id in self.students:
            print("A student with that ID already exists.")
            return

        name = input("Enter name: ").strip()
        age_str = input("Enter age: ").strip()
        gender = input("Enter gender: ").strip()

        try:
            age = int(age_str)
        except ValueError:
            print("Age must be an integer.")
            return

        student = Student(id=student_id, name=name, age=age, gender=gender)
        self.students[student_id] = student
        print(f"Registered student {student_id} - {name}")

    def _list_courses(self) -> None:
        print("\nAvailable courses:")
        for course in self.courses.values():
            print(
                f"- {course.id}: {course.title} "
                f"(difficulty={course.difficulty}, sequences={len(course.sequences)})"
            )

        print("\nPrerequisite relationships (prereq -> course):")
        for prereq, dependents in self.course_graph.graph.items():
            if dependents:
                print(f"  {prereq} -> {', '.join(dependents)}")

    def _search_content(self) -> None:
        prefix = input("Enter keyword or prefix to search: ").strip()
        results = self.trie.autocomplete(prefix)
        if not results:
            print("No matching content found.")
            return

        print("Matches:")
        for item in results:
            print(f"- {item}")

    def _get_student_by_prompt(self) -> Optional[Student]:
        student_id = input("Enter student ID: ").strip()
        student = self.students.get(student_id)
        if not student:
            print("Student not found.")
            return None
        return student

    def _enroll_student(self) -> None:
        student = self._get_student_by_prompt()
        if not student:
            return

        self._list_courses()
        course_id = input("Enter course ID to enroll: ").strip()

        if course_id not in self.courses:
            print("Invalid course ID.")
            return

        # Check prerequisites
        prereqs = self.course_graph.find_all_prerequisites(course_id)
        missing = [
            cid
            for cid in prereqs
            if not self._has_completed_any_sequence_in_course(student, cid)
        ]
        if missing:
            print(
                "Warning: student has not completed any sequences in prerequisite courses: "
                + ", ".join(missing)
            )

        student.change_current_course(course_id)
        print(f"Student {student.id} is now focusing on course '{course_id}'.")

    def _has_completed_any_sequence_in_course(
        self, student: Student, course_id: str
    ) -> bool:
        course = self.courses.get(course_id)
        if not course:
            return False
        return any(seq.id in student.completed_sequences for seq in course.sequences)

    def _complete_next_sequence(self) -> None:
        student = self._get_student_by_prompt()
        if not student:
            return

        if student.current_course_id is None:
            print("Student has no active course. Enroll them first.")
            return

        # Find the next scheduled sequence for this course
        next_task = self._dequeue_next_for_course(student.current_course_id)
        if next_task is None:
            print("No remaining scheduled sequences for this course.")
            return

        # Simulate completion and a basic quiz score
        course_id = next_task.course_id
        sequence_id = next_task.sequence_id

        print(
            f"Completing sequence '{sequence_id}' for course '{course_id}' "
            f"(estimated duration={next_task.duration})."
        )

        # Simple score: length of sequence_id * 10 (just to have deterministic scores)
        score = len(sequence_id) * 10
        student.update_progress(
            course_id=course_id, sequence_id=sequence_id, score=score
        )

        print(
            f"Sequence '{sequence_id}' completed with score {score}. "
            f"Total progress: {student.progress} sequences."
        )

    def _dequeue_next_for_course(self, course_id: str) -> Optional[SequenceTask]:
        """
        Dequeue the next SequenceTask for the given course_id
        while preserving the schedule for other courses.
        """
        # Strategy:
        # - Pop tasks until we find one for this course or heap is empty.
        # - Temporarily store others and push them back.
        temp: list[SequenceTask] = []
        selected: Optional[SequenceTask] = None

        while not self.scheduler.is_empty():
            task = self.scheduler.dequeue_next()
            if task.course_id == course_id and selected is None:
                selected = task
                break
            temp.append(task)

        # Push back other tasks
        for t in temp:
            self.scheduler.schedule(t)

        return selected

    def _view_student_history(self) -> None:
        student = self._get_student_by_prompt()
        if not student:
            return

        print(f"\nHistory for student {student.id} - {student.name}:")
        if len(student.history) == 0:
            print("No activity recorded yet.")
            return

        for activity in student.history.iterate_activities():
            desc = activity.describe()
            print(f"- {desc}")

    def _show_recommendations(self) -> None:
        student = self._get_student_by_prompt()
        if not student:
            return

        recs = self.recommendation_engine.recommend_for(student, self.courses, top_n=5)
        print(f"\nRecommendations for {student.id} - {student.name}:")
        for item in recs:
            course = self.courses[item.course_id]
            print(
                f"- {course.title} (id={item.course_id}, diff={course.difficulty}) "
                f"=> score={item.score:.3f}"
            )
            print(f"    why: {item.explanation}")


def main() -> None:
    app = LearningPlatformCLI()
    app.run()


if __name__ == "__main__":
    main()
