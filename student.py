# stores student information
# and provides a method to update student details which is saved using the update_student method
# in the student database class

class Student:
    def __init__(self,name, age, grade, student_id=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade


    def update(self,name,age,grade):
        if name:
            self.name = name
        if age:
            self.age = age
        if grade:
            self.grade = grade
        
    
    
    