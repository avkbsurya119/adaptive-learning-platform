from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Set

from core.models.course import Course


@dataclass
class CourseGraph:
    """
    Directed acyclic graph (DAG) of courses and their prerequisites.

    Conventions:
        - An edge prereq_id -> course_id means:
              "prereq_id must be completed BEFORE course_id".
        - `graph`      : prereq_id -> set of dependent course_ids
        - `reverse_graph`: course_id -> set of prerequisite course_ids
        - `in_degrees` : course_id -> number of prerequisites

    This class does NOT perform persistence or I/O.
    """

    courses: Dict[str, Course] = field(default_factory=dict)
    graph: Dict[str, Set[str]] = field(default_factory=dict)
    reverse_graph: Dict[str, Set[str]] = field(default_factory=dict)
    in_degrees: Dict[str, int] = field(default_factory=dict)
    course_content: Dict[str, List[str]] = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    # Course management
    # ------------------------------------------------------------------ #

    def add_course(self, course: Course) -> None:
        """
        Register a course in the graph. If the course already exists,
        it is replaced (but edges are preserved).

        Ensures all internal maps have entries for this course ID.
        """
        course_id = course.id
        self.courses[course_id] = course

        if course_id not in self.graph:
            self.graph[course_id] = set()

        if course_id not in self.reverse_graph:
            self.reverse_graph[course_id] = set()

        if course_id not in self.in_degrees:
            self.in_degrees[course_id] = 0

        if course_id not in self.course_content:
            self.course_content[course_id] = []

    def _ensure_course_exists(self, course_id: str) -> None:
        if course_id not in self.courses:
            raise KeyError(f"Course '{course_id}' is not registered in CourseGraph.")

    # ------------------------------------------------------------------ #
    # Prerequisite edges
    # ------------------------------------------------------------------ #

    def add_prerequisite(self, prereq_id: str, course_id: str) -> None:
        """
        Add an edge prereq_id -> course_id.

        Args:
            prereq_id: ID of the prerequisite course.
            course_id: ID of the course that depends on the prerequisite.

        Raises:
            KeyError: if either course is unknown.
        """
        self._ensure_course_exists(prereq_id)
        self._ensure_course_exists(course_id)

        # Initialize adjacency sets if needed
        if prereq_id not in self.graph:
            self.graph[prereq_id] = set()
        if course_id not in self.reverse_graph:
            self.reverse_graph[course_id] = set()

        # If the edge is new, update structures
        if course_id not in self.graph[prereq_id]:
            self.graph[prereq_id].add(course_id)
            self.reverse_graph[course_id].add(prereq_id)
            self.in_degrees[course_id] = self.in_degrees.get(course_id, 0) + 1

        # Ensure prereq has entries in maps
        self.in_degrees.setdefault(prereq_id, 0)
        self.reverse_graph.setdefault(prereq_id, set())

    def get_prerequisites(self, course_id: str) -> Set[str]:
        """
        Return the direct prerequisites of a course.

        Raises:
            KeyError: if course_id is unknown.
        """
        self._ensure_course_exists(course_id)
        return set(self.reverse_graph.get(course_id, set()))

    def find_all_prerequisites(self, course_id: str) -> Set[str]:
        """
        Return all (direct and indirect) prerequisites of a course
        using BFS over reverse_graph.

        Raises:
            KeyError: if course_id is unknown.
        """
        self._ensure_course_exists(course_id)

        visited: Set[str] = set()
        queue: deque[str] = deque(self.reverse_graph.get(course_id, set()))

        while queue:
            prereq = queue.popleft()
            if prereq in visited:
                continue
            visited.add(prereq)
            # Add prerequisites of this prereq
            for parent in self.reverse_graph.get(prereq, set()):
                if parent not in visited:
                    queue.append(parent)

        return visited

    # ------------------------------------------------------------------ #
    # Topological sort
    # ------------------------------------------------------------------ #

    def topological_sort(self) -> List[str]:
        """
        Perform a topological sort of all registered courses.

        Returns:
            A list of course IDs in an order that respects prerequisites.

        Raises:
            ValueError: if a cycle is detected in the graph.
        """
        # Work on a copy so we do not mutate self.in_degrees
        in_deg_copy: Dict[str, int] = dict(self.in_degrees)

        # Start with all nodes with in-degree 0
        zero_in_degree = deque(
            course_id for course_id, deg in in_deg_copy.items() if deg == 0
        )
        topo_order: List[str] = []

        while zero_in_degree:
            course_id = zero_in_degree.popleft()
            topo_order.append(course_id)

            for neighbor in self.graph.get(course_id, set()):
                in_deg_copy[neighbor] -= 1
                if in_deg_copy[neighbor] == 0:
                    zero_in_degree.append(neighbor)

        if len(topo_order) != len(self.courses):
            # There must be a cycle or missing in-degree entries
            raise ValueError("Cycle detected in course prerequisites.")

        return topo_order

    # ------------------------------------------------------------------ #
    # Course content
    # ------------------------------------------------------------------ #

    def add_content(self, course_id: str, content_item: str) -> None:
        """
        Append a content identifier (e.g., topic name, content ID) to a course.

        Does not replace existing content; always appends.
        """
        self._ensure_course_exists(course_id)
        self.course_content.setdefault(course_id, [])
        self.course_content[course_id].append(content_item)

    def get_content(self, course_id: str) -> List[str]:
        """
        Retrieve the list of content items associated with a course.

        Raises:
            KeyError: if course_id is unknown.
        """
        self._ensure_course_exists(course_id)
        return list(self.course_content.get(course_id, []))
