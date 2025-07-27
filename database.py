#handles database operations for student records
# including inserting, fetching, deleting, and updating student records

from student import Student
import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        # Connect to the database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_db"
        )
        self.cursor = self.connection.cursor()

    def insert_student(self, name, age, grade):
        query = "INSERT INTO student (name, age, grade) VALUES (%s, %s, %s)"
        values = (name, age, grade)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Student inserted successfully")

    def fetch_students(self):
        self.cursor.execute("SELECT * FROM student")
        rows = self.cursor.fetchall()
        # Convert rows to Student objects
        students = []   
        for row in rows:
            student = Student(
                name=row[1],
                age=row[2],
                grade=row[3],
                student_id=row[0]  
            )
            students.append(student)
            
        return students

    def delete_student(self,Id):
        query = "DELETE FROM student WHERE id = %s"
        value = (Id,)
        self.cursor.execute(query, value)
        self.connection.commit()
        print(f"Student id {value} deleted successfully")
        
    def update_student(self, student):
        query = "UPDATE student SET name = %s, age = %s, grade = %s WHERE id = %s"
        values = (student.name, student.age, student.grade, student.student_id)
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"Student id {student.student_id} updated successfully")

    

    

