from SequenceQueue import SequenceQueue
class CourseGraph:
    def __init__(self):
        # Stores the graph as an adjacency list, in-degrees for topological sorting, and content for each module
        self.graph = {}
        self.in_degrees = {}
        self.content = {} 
        self.sequences = {}

    def add_module(self, module, sequences=None):
        if module not in self.graph:
            self.graph[module] = []
            self.in_degrees[module] = 0
            self.content[module] = []
            self.sequences[module] = sequences if sequences else []

    def add_prerequisite(self, prerequisite, module):
        if prerequisite not in self.graph:
            self.add_module(prerequisite)
        if module not in self.graph:
            self.add_module(module)
        self.graph[prerequisite].append(module)
        self.in_degrees[module] += 1

    def add_content(self, course_title, content_item):
        if course_title in self.graph:
            if course_title not in self.content:
                self.content[course_title] = []
            self.content[course_title].append(content_item)
        else:
            raise ValueError(f"Course {course_title} does not exist.")

    def get_courses_by_content(self, content_item):
        courses_with_content = []
        for course, contents in self.content.items():
            if content_item in contents:
                courses_with_content.append(course)
        return courses_with_content
    def topological_sort(self):
        # Perform topological sort to determine course order
        zero_in_degree = [node for node in self.graph if self.in_degrees[node] == 0]
        topo_order = []

        while zero_in_degree:
            module = zero_in_degree.pop(0)
            topo_order.append(module)

            for neighbor in self.graph[module]:
                self.in_degrees[neighbor] -= 1
                if self.in_degrees[neighbor] == 0:
                    zero_in_degree.append(neighbor)

        # If topo_order contains all modules, return it. Otherwise, a cycle exists.
        if len(topo_order) == len(self.graph):
            return topo_order
        else:
            raise ValueError("Cycle detected in prerequisites, topological sort not possible.")

    def find_all_prerequisites(self, module):
        # Find all prerequisites of a module using BFS
        prerequisites = set()
        queue = [module]

        while queue:
            current = queue.pop(0)
            for prereq in self.graph:
                if current in self.graph[prereq] and prereq not in prerequisites:
                    prerequisites.add(prereq)
                    queue.append(prereq)

        return prerequisites

    def find_shortest_path(self, start, end):
        # Find the shortest path from start to end using BFS
        queue = [(start, [start])]
        visited = set([start])

        while queue:
            current, path = queue.pop(0)
            if current == end:
                return path

            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # No path found

    def can_access_module(self, module, completed_modules):
        # Check if all prerequisites are completed
        prerequisites = self.find_all_prerequisites(module)
        return prerequisites.issubset(completed_modules)

    def get_prerequisites(self, module):
        """Get the direct prerequisites of a specified module."""
        if module not in self.graph:
            raise ValueError(f"Module {module} does not exist.")
        return self.graph[module]

    def add_content(self, course_title, content):
        """Add content to a specified course."""
        if course_title in self.graph:
            self.content[course_title] = content  # Store the content for the course
        else:
            raise ValueError(f"Course {course_title} does not exist.")

    def get_content(self, course_title):
        """Retrieve content for a specified course."""
        if course_title in self.content:
            return self.content[course_title]
        else:
            raise ValueError(f"Course {course_title} does not exist.")

    def check_prerequisites(self, module):
        """Return True if prerequisites are met for the specified module, otherwise False."""
        if module not in self.graph:
            raise ValueError(f"Module {module} does not exist.")
        
        prerequisites = self.find_all_prerequisites(module)
        return prerequisites  # This could be an empty set if no prerequisites are required
    
    def check_sequences_completion(self, module, completed_sequences):
        # Verifies if all sequences for the module are completed
        required_sequences = set(self.sequences.get(module, []))
        return required_sequences.issubset(set(completed_sequences))
