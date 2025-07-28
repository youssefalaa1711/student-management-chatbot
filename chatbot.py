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
        elif text == "search student":
            return "search_student"
        elif text == "search grade":
            return "search_grade"
        elif text == "search age":
            return "search_age"
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

        elif intent == "search_student":
            self.pending_action = "search_student"
            return "Please enter the student's name to search:"
        elif intent == "search_grade":
            self.pending_action = "search_grade"
            return "Please enter the grade to search for:"
        elif intent == "search_age":
            self.pending_action = "search_age"
            return "Please enter the age to search for (e.g., 18 or 18-22):"

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

        elif self.pending_action == "search_student":
            name_query = user_input.strip().lower()
            students = self.database.fetch_students()
            results = [
                s for s in students if name_query in s.name.lower()
            ]
            self.pending_action = None
            if results:
                return "\n".join([
                    f"{s.student_id}: {s.name}, Age: {s.age}, Grade: {s.grade}"
                    for s in results
                ])
            else:
                return "No student found with that name."

        elif self.pending_action == "search_grade":
            grade_query = user_input.strip().lower()
            students = self.database.fetch_students()
            results = [s for s in students if grade_query == str(s.grade).lower()]
            self.pending_action = None
            if results:
                return "\n".join([f"{s.student_id}: {s.name}, Age: {s.age}, Grade: {s.grade}" for s in results])
            else:
                return "No student found with that grade."

        elif self.pending_action == "search_age":
            age_query = user_input.strip()
            students = self.database.fetch_students()
            results = []
            if "-" in age_query:
                try:
                    min_age, max_age = map(int, age_query.split("-"))
                    results = [s for s in students if min_age <= int(s.age) <= max_age]
                except:
                    self.pending_action = None
                    return "Invalid range format. Please enter as 'min-max' (e.g., 18-22)."
            else:
                results = [s for s in students if age_query == str(s.age)]
            self.pending_action = None
            if results:
                return "\n".join([f"{s.student_id}: {s.name}, Age: {s.age}, Grade: {s.grade}" for s in results])
            else:
                return "No student found with that age or in that range."

        return "Unexpected error. Try again."

    def reset_session(self):
        self.history.clear()
        self.pending_action = None
        self.temp_data = {}
