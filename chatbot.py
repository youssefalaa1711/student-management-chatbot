from datetime import datetime
from student import Student

class Chatbot:
    def __init__(self, database):
        self.database = database
        self.history = []
        self.pending_action = None # used to keep track of ongoing actions
        self.pending_data = {} # used to store input across multiple steps(name -> age -> grade ))

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def ask(self, user_input):
        user_input = user_input.strip()
        response = ""

        if self.pending_action == "add_student":
            response = self._handle_add_student(user_input)

        else:
            intent = self._match_intent(user_input)
            response = self._respond(intent, user_input)

        self.history.append({
            "timestamp": self.get_current_time(),
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
        elif text.startswith("delete student"):
            return "delete_student"
        elif text.startswith("update student"):
            return "update_student"
        else:
            return "unknown"

    def _respond(self, intent, user_input):
        if intent == "fetch_students":
            students = self.database.fetch_students()
            if not students:
                return "No students found."
            return "\n".join([f"{s.student_id}: {s.name}, Age: {s.age}, Grade: {s.grade}" for s in students])

        elif intent == "add_student":
            self.pending_action = "add_student"
            self.pending_data = {}
            return "Please enter the student's full name:"

        elif intent == "delete_student":
            parts = user_input.split()
            if len(parts) < 3 or not parts[2].isdigit():
                return "Invalid format. Use: delete student <ID>"
            student_id = int(parts[2])
            self.database.delete_student(student_id)
            return f"Student with ID {student_id} deleted successfully."

        elif intent == "update_student":
            return "Update functionality will be added soon."

        else:
            return "I didn't understand that. Try commands like: 'add student', 'fetch students', 'delete student <ID>'."

    def _handle_add_student(self, user_input):
        if "name" not in self.pending_data:
            self.pending_data["name"] = user_input
            return "Enter the student's age:"

        elif "age" not in self.pending_data:
            if not user_input.isdigit():
                return "Age must be a number. Please enter a valid age:"
            self.pending_data["age"] = user_input
            return "Enter the student's grade:"

        elif "grade" not in self.pending_data:
            self.pending_data["grade"] = user_input

            # All data received; add student to database
            name = self.pending_data["name"]
            age = self.pending_data["age"]
            grade = self.pending_data["grade"]

            self.database.insert_student(name, age, grade)

            self.pending_action = None
            self.pending_data = {}

            return f"Student {name} added successfully (Age: {age}, Grade: {grade})."

    def show_history(self):
        for entry in self.history:
            print(f"{entry['timestamp']} - User: {entry['user']} | Bot: {entry['bot']}")

    def reset_session(self):
        self.history.clear()
        self.pending_action = None
        self.pending_data = {}
        return "Session reset."
