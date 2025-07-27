# chatbot.py
from student import Student
from database import Database
from datetime import datetime

class Chatbot:
    def __init__(self, database):
        self.database = database
        self.history = []
        self.pending_action = None
        self.temp_data = {}

    def ask(self, user_input):
        response = ""

        if self.pending_action:
            response = self._handle_pending(user_input)
        else:
            intent = self._match_intent(user_input)
            response = self._respond(intent, user_input)

        self.history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "bot": response
        })
        return response

    def _match_intent(self, text):
        text = text.lower()
        if text == "fetch students":
            return "fetch_students"
        elif text == "add student":
            return "add_student"
        elif text == "delete student":
            return "delete_student"
        elif text == "update student":
            return "update_student"
        return "unknown"

    def _respond(self, intent, user_input):
        if intent == "fetch_students":
            students = self.database.fetch_students()
            if not students:
                return "No students found."
            return "\n".join([
                f"{s.student_id}: {s.name}, Age: {s.age}, Grade: {s.grade}"
                for s in students
            ])

        elif intent == "add_student":
            self.pending_action = "add_student"
            self.temp_data = {}
            return "Please enter the student's name:"

        elif intent == "delete_student":
            self.pending_action = "delete_student"
            return "Please enter the student ID to delete:"

        elif intent == "update_student":
            self.pending_action = "update_student_id"
            return "Please enter the student ID to update:"

        return "I didn't understand that. Please try again."

    def _handle_pending(self, user_input):
        if self.pending_action == "add_student":
            if "name" not in self.temp_data:
                self.temp_data["name"] = user_input
                return "Please enter the student's age:"
            elif "age" not in self.temp_data:
                self.temp_data["age"] = user_input
                return "Please enter the student's grade:"
            else:
                self.temp_data["grade"] = user_input
                self.database.insert_student(
                    self.temp_data["name"],
                    self.temp_data["age"],
                    self.temp_data["grade"]
                )
                self.pending_action = None
                return f"Student {self.temp_data['name']} added successfully."

        elif self.pending_action == "delete_student":
            try:
                student_id = int(user_input)
                self.database.delete_student(student_id)
                self.pending_action = None
                return f"Student with ID {student_id} deleted successfully."
            except:
                return "Invalid ID. Please enter a numeric value."

        elif self.pending_action == "update_student_id":
            try:
                self.temp_data["id"] = int(user_input)
                self.pending_action = "update_student_name"
                return "Enter the new name:"
            except:
                return "Invalid ID. Please enter a numeric value."

        elif self.pending_action == "update_student_name":
            self.temp_data["name"] = user_input
            self.pending_action = "update_student_age"
            return "Enter the new age:"

        elif self.pending_action == "update_student_age":
            self.temp_data["age"] = user_input
            self.pending_action = "update_student_grade"
            return "Enter the new grade:"

        elif self.pending_action == "update_student_grade":
            self.temp_data["grade"] = user_input
            student = Student(
                name=self.temp_data["name"],
                age=self.temp_data["age"],
                grade=self.temp_data["grade"],
                student_id=self.temp_data["id"]
            )
            self.database.update_student(student)
            self.pending_action = None
            return f"Student with ID {student.student_id} updated successfully."

        return "Unexpected error. Try again."

    def reset_session(self):
        self.history.clear()
        self.pending_action = None
        self.temp_data = {}
