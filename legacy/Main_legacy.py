import random
from datetime import datetime, timedelta

# Import all ADTs
from ContentTrie import ContentTrie
from CourseGraph import CourseGraph
from StudentHashMap import StudentHashMap, Student
from RecommadationHeap import RecommadationHeap
from SequenceQueue import SequenceQueue
from StudentHistoryArray import StudentHistoryArray, Activity

# Initialize ADTs
course_graph = CourseGraph()
content_trie = ContentTrie()
student_map = StudentHashMap()
recommendation_heap = RecommadationHeap()
schedule_queue = SequenceQueue()
history_tracker = StudentHistoryArray()

# Predefined courses setup
# Initialize courses with content and schedule setup
def initialize_courses_with_schedule():
    courses = {
        "Data Structures": {
            "content": ["Arrays", "Linked Lists", "Stacks"],
            "priority": 1,
            "prereqs": [],
            "sequences": [("Arrays Basics", timedelta(days=1)), ("Linked Lists Operations", timedelta(days=1)), ("Stack Implementation", timedelta(days=2))]
        },
        "Algorithms": {
            "content": ["Sorting", "Searching"],
            "priority": 2,
            "prereqs": ["Data Structures"],
            "sequences": [("Sorting Techniques", timedelta(days=2)), ("Binary Search", timedelta(days=1))]
        },
        "Advanced Programming": {
            "content": ["Recursion", "Dynamic Programming"],
            "priority": 3,
            "prereqs": ["Algorithms"],
            "sequences": [("Recursion Basics", timedelta(days=1)), ("Dynamic Programming Patterns", timedelta(days=3))]
        }
    }

    for course_name, details in courses.items():
        # Set course modules and schedule sequences
        course_graph.add_module(course_name, [seq[0] for seq in details["sequences"]])
        schedule_queue.update_priority(course_name, details["priority"])
        
        # Add course content and prerequisites
        for content in details["content"]:
            content_trie.insertContent(content)
            course_graph.add_content(course_name, content)
        for prereq in details["prereqs"]:
            course_graph.add_prerequisite(course_name, prereq)

        # Schedule each sequence with defined duration
        for sequence, duration in details["sequences"]:
            schedule_queue.schedule_course(sequence, duration, details["priority"])

    # Debug: Print the content of each course to verify
    for course in course_graph.graph:
        print(f"Course: {course}, Content: {course_graph.get_content(course)}")

    print("Predefined courses with schedules initialized.")

# Predefined students setup
def initialize_students_with_current_courses():
    # Define students with some completed courses and current courses
    students = [
        {
            "student_id": "S101",
            "name": "Alice",
            "age": 20,
            "gender": "Female",
            "completed_courses": ["Data Structures"],
            "scores": {"Data Structures": 85},
            "current_courses": ["Algorithms"]
        },
        {
            "student_id": "S102",
            "name": "Bob",
            "age": 22,
            "gender": "Male",
            "completed_courses": ["Data Structures", "Algorithms"],
            "scores": {"Data Structures": 78, "Algorithms": 88},
            "current_courses": []
        }
    ]
    
    for student in students:
        student_obj = Student(student["student_id"], student["name"], student["age"], student["gender"])
        for course, score in student["scores"].items():
            student_obj.update_progress(course, score)
            history_tracker.append_activity("Course", datetime.now(), score, {"course": course})
            recommendation_heap.insert((course, score))
        
        # Add current courses to the student
        student_obj.current_course = student.get("current_courses", [])
        student_map.insert_student(student_obj)
    
    print("Predefined students with current courses initialized.")


# Utility for quiz score generation
def random_quiz_score():
    return random.randint(50, 100)

# Admin functionalities
def add_course():
    course_name = input("Enter the course name to add: ")
    if course_graph.graph.get(course_name):
        print(f"Course '{course_name}' already exists.")
    else:
        course_graph.add_module(course_name)
        print(f"Course '{course_name}' added successfully.")

def add_content_to_course():
    course_name = input("Enter course name for adding content: ")
    if course_name in course_graph.graph:
        content = input("Enter content (title, keyword, tag): ")
        content_trie.insertContent(content)
        course_graph.add_content(course_name, content)
        print(f"Content '{content}' added to course '{course_name}'.")
    else:
        print("Course not found.")

def change_course_priority():
    course_name = input("Enter course name to change priority: ")
    priority = int(input("Enter new priority level (lower is higher priority): "))
    schedule_queue.update_priority(course_name, priority)
    print(f"Priority of course '{course_name}' updated to {priority}.")

# New user registration and course selection
def create_new_user():
    student_id = input("Enter Student ID: ")
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    
    student = Student(student_id, name, age, gender)
    student_map.insert_student(student)
    
    enhanced_search_content(student)

def enhanced_search_content(student):
    prefix = input("Enter a keyword or course title to search: ")
    results = content_trie.autocomplete(prefix)

    
    if results:
        print("Courses found: ", results)
        course_name = input("Enter the course you'd like to take: ")
        
        # Confirm with the student if they want to take the course
        confirm = input(f"Do you want to take the course '{course_name}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            # Check if there are prerequisites
            prereqs = course_graph.get_prerequisites(course_name)
            if prereqs:
                print(f"The course '{course_name}' has the following prerequisites: {prereqs}")
                for prereq in prereqs:
                    if prereq not in student.completed_sequences:
                        take_prereq = input(f"Would you like to complete the prerequisite course '{prereq}' first? (yes/no): ").strip().lower()
                        if take_prereq == "yes":
                            start_course(student, prereq)
                        else:
                            print(f"Skipping prerequisite course '{prereq}'.")
                    else:
                        print(f"You have already completed the prerequisite '{prereq}'.")
            
            # After handling prerequisites, confirm if they still want to take the main course
            final_confirm = input(f"Do you still want to start the course '{course_name}'? (yes/no): ").strip().lower()
            if final_confirm == "yes":
                start_course(student, course_name)
            else:
                print(f"Course '{course_name}' was not started.")
        else:
            print(f"Course '{course_name}' was not selected.")
    else:
        print("No courses found for that keyword.")


def start_course(student, course_name):
    print(f"Starting course '{course_name}'")
    sequences = course_graph.sequences.get(course_name, [])
    
    # Complete sequences in the course
    for sequence in sequences:
        quiz_score = random_quiz_score()
        student.update_progress(course_name, sequence, quiz_score)
        
        # Check recommendation based on randomized progress threshold
        recommendation_threshold = random.randint(2, 5)
        recommendation_heap.insert_recommendation(course_name, student.progress, recommendation_threshold)
    
    print(f"Completed '{course_name}' with progress {student.progress}")

# Existing user functions
def view_profile(student_id):
    student_data = student_map.retrieve_student_data(student_id)
    if student_data:
        print("\n===== Student Profile =====")
        print(f"Name       : {student_data['name']}")
        print(f"Age        : {student_data['age']}")
        print(f"Gender     : {student_data['gender']}")
        print(f"Current Course: {student_data['current_course'] or 'None'}")
        print(f"Progress   : {student_data['progress']} sequences completed\n")
        
        # Display activity history with formatting
        print("===== Activity History =====")
        for activity in student_data['history']:
            print(f"- {activity.activity_type} | Date: {activity.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            if activity.score is not None:
                print(f"  Score: {activity.score}")
            if activity.metadata:
                print(f"  Details: {activity.metadata}")
        print("\n===========================\n")
    else:
        print("Student ID not found.")


def view_history(student_id):
    print("Activity History:")
    for activity in history_tracker.iterate_activities():
        print(activity)

def view_active_schedule(student):
    print(f"\nActive Course Schedule for {student.student_id}:")
    if student.current_course:
        course_sequences = course_graph.sequences.get(student.current_course, [])
        print(f"Current course: {student.current_course}")
        for seq in course_sequences:
            print(f"- Sequence: {seq}")
    else:
        print("No active course at the moment. Please start a course to view its schedule.")

def start_scheduled_course(student):
    course_name = input("Enter course name to start: ")
    if course_graph.can_access_module(course_name, student.completed_sequences):
        student.current_course = course_name
        start_course_with_schedule(student, course_name)
    else:
        prereqs = course_graph.get_prerequisites(course_name)
        print(f"Cannot start '{course_name}'. Please complete prerequisites first: {prereqs}")

def start_course_with_schedule(student, course_name):
    if course_graph.can_access_module(course_name, student.completed_sequences):
        student.current_course = course_name
        sequences = course_graph.sequences[course_name]
        
        for sequence in sequences:
            scheduled_sequence = schedule_queue.dequeue()
            # Log completion in history and add quiz scores
            quiz_score = random_quiz_score()
            student.update_progress(course_name, scheduled_sequence, quiz_score)
            history_tracker.append_activity("Completed Sequence", datetime.now(), quiz_score, {"course": course_name, "sequence": scheduled_sequence})
            recommendation_heap.insert_recommendation(course_name, student.progress, recommendation_threshold=random.randint(2, 5))

        print(f"Completed course '{course_name}' with progress: {student.progress}")
    else:
        print(f"Prerequisites not met for '{course_name}'")


def get_recommendations(student):
    print("\nRecommended Courses based on your progress:")
    recommended_courses = recommendation_heap.display() or []  # Handle None by using an empty list
    for course, rec_value in recommended_courses:
        if rec_value > student.progress:
            print(f"Recommended Course: {course} | Recommendation Value: {rec_value}")
        else:
            print(f"'{course}' is below your current progress and not recommended.")

def main_menu():
    while True:
        print("\n===== Main Menu =====")
        print("1. Admin")
        print("2. New User")
        print("3. Existing User")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            admin_menu()
        elif choice == '2':
            create_new_user()
        elif choice == '3':
            existing_user_menu()
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

def admin_menu():
    while True:
        print("\n===== Admin Menu =====")
        print("1. Add new course")
        print("2. Add content to course")
        print("3. Change course priority")
        print("4. Back to main menu")
        choice = input("Enter choice: ")

        if choice == '1':
            add_course()
        elif choice == '2':
            add_content_to_course()
        elif choice == '3':
            change_course_priority()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

def existing_user_menu():
    student_id = input("Enter your Student ID: ")
    student = student_map.student_map.get(student_id)  # Retrieve the Student object directly
    if student:
        while True:
            print("\n===== Existing User Menu =====")
            print("1. View Profile")
            print("2. View Activity History")
            print("3. Get Course Recommendations")
            print("4. View Active Course Schedule")
            print("5. Start Scheduled Course")
            print("6. Search for Courses")
            print("7. Back to main menu")
            choice = input("Enter choice: ")

            if choice == '1':
                view_profile(student_id)
            elif choice == '2':
                view_history(student_id)
            elif choice == '3':
                get_recommendations(student)
            elif choice == '4':
                view_active_schedule(student)
            elif choice == '5':
                start_scheduled_course(student)
            elif choice == '6':
                enhanced_search_content(student)  # Use enhanced search content
            elif choice == '7':
                break
            else:
                print("Invalid choice. Try again.")
    else:
        print("Student ID not found.")

initialize_courses_with_schedule()
initialize_students_with_current_courses()
main_menu()