from StudentHistoryArray import StudentHistoryArray
from datetime import datetime
class Student:
    def __init__(self, student_id, name, age, gender):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.current_course = None
        self.completed_sequences = set()  # Track completed sequences
        self.progress = 0
        self.history = StudentHistoryArray()

    def update_progress(self, module, sequence, score=None):
        # Complete a sequence and update progress if it belongs to the current module
        if sequence not in self.completed_sequences:
            self.completed_sequences.add(sequence)
            self.progress += 1  # Update progress for each sequence
            self.history.append_activity("Sequence Completion", datetime.now(), score, {"module": module, "sequence": sequence})
            if score is not None:
                self.history.append_activity("Quiz", datetime.now(), score, {"module": module, "sequence": sequence})


class StudentHashMap:
    def __init__(self):
        self.student_map = {}

    def insert_student(self, student):
        self.student_map[student.student_id] = student

    def update_student_progress(self, student_id, module, score=None):
        student = self.student_map.get(student_id)
        if student:
            student.update_progress(module, score)
        else:
            print(f"Student with ID {student_id} not found.")

    def retrieve_student_data(self, student_id):
        student = self.student_map.get(student_id)
        if student:
            return {
                'name': student.name,
                'age': student.age,
                'gender': student.gender,
                'current_course': student.current_course,
                'progress': student.progress,
                'history': list(student.history.iterate_activities())
            }
        else:
            print(f"Student with ID {student_id} not found.")
            return None