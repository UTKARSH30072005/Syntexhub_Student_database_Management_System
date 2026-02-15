import json
import os

class Student:
    """Blueprint for a single student record."""
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        """Converts object to dictionary for JSON storage."""
        return {"id": self.student_id, "name": self.name, "grade": self.grade}

class StudentManager:
    """Encapsulates all operations: Add, Update, Delete, List, and File I/O."""
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        """Reads records from the JSON file."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_data(self):
        """Saves current student list to the JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(self.students, f, indent=4)

    def is_id_unique(self, student_id):
        """Validation: Ensures no two students have the same ID."""
        return not any(s['id'] == student_id for s in self.students)

    def add_student(self, student_id, name, grade):
        if not self.is_id_unique(student_id):
            print(f"\n[Error] Student ID {student_id} already exists!")
            return
        
        new_student = Student(student_id, name, grade)
        self.students.append(new_student.to_dict())
        self.save_data()
        print(f"\n[Success] Student '{name}' added.")

    def update_student(self, student_id, new_name=None, new_grade=None):
        for s in self.students:
            if s['id'] == student_id:
                if new_name: s['name'] = new_name
                if new_grade: s['grade'] = new_grade
                self.save_data()
                print(f"\n[Success] Student {student_id} updated.")
                return
        print(f"\n[Error] Student ID {student_id} not found.")

    def delete_student(self, student_id):
        original_length = len(self.students)
        self.students = [s for s in self.students if s['id'] != student_id]
        
        if len(self.students) < original_length:
            self.save_data()
            print(f"\n[Success] Student {student_id} removed.")
        else:
            print(f"\n[Error] Student ID {student_id} not found.")

    def list_students(self):
        """Formatted console output for student records."""
        if not self.students:
            print("\n--- No records available ---")
            return
        
        print("\n" + "="*45)
        print(f"{'ID':<10} | {'Name':<20} | {'Grade':<10}")
        print("-" * 45)
        for s in self.students:
            print(f"{s['id']:<10} | {s['name']:<20} | {s['grade']:<10}")
        print("="*45)

# --- Main Application Logic ---
def main():
    manager = StudentManager()

    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List All Students")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")

        if choice == '1':
            sid = input("Enter ID: ")
            name = input("Enter Name: ")
            grade = input("Enter Grade: ")
            manager.add_student(sid, name, grade)

        elif choice == '2':
            sid = input("Enter ID to update: ")
            name = input("Enter new Name (leave blank to skip): ")
            grade = input("Enter new Grade (leave blank to skip): ")
            manager.update_student(sid, name if name else None, grade if grade else None)

        elif choice == '3':
            sid = input("Enter ID to delete: ")
            manager.delete_student(sid)

        elif choice == '4':
            manager.list_students()

        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid input. Please choose 1-5.")

if __name__ == "__main__":
    main()