# ============================================================
# Class Variables vs Instance Variables
# Class variables: shared by ALL instances
# Instance variables: unique to EACH object
# ============================================================

class Student:
    """Demonstrates the difference between class and instance variables."""

    # Class variables — defined at class level, shared by all
    school_name = "Python Academy"
    total_students = 0       # tracks how many students exist

    def __init__(self, name, grade):
        # Instance variables — unique to each student
        self.name = name
        self.grade = grade
        self.courses = []

        # Modify class variable when a new student is created
        Student.total_students += 1
        self.student_id = Student.total_students   # unique ID

    def enroll(self, course):
        """Enrolls the student in a course."""
        self.courses.append(course)
        print(f"{self.name} enrolled in {course}")

    def describe(self):
        print(f"\nStudent #{self.student_id}: {self.name}")
        print(f"  School:  {Student.school_name}")   # class variable
        print(f"  Grade:   {self.grade}")             # instance variable
        print(f"  Courses: {', '.join(self.courses) if self.courses else 'None'}")


print("--- Creating students ---")
s1 = Student("Alice", "A")
s2 = Student("Bob", "B")
s3 = Student("Charlie", "A")

# Class variable is the SAME for all instances
print(f"\nSchool (via s1): {s1.school_name}")
print(f"School (via s2): {s2.school_name}")
print(f"School (via class): {Student.school_name}")

# Instance variables are DIFFERENT per object
print(f"\ns1 name: {s1.name}, grade: {s1.grade}")
print(f"s2 name: {s2.name}, grade: {s2.grade}")

# Class variable tracks total across all instances
print(f"\nTotal students: {Student.total_students}")  # 3

# Enroll students in courses
s1.enroll("Python")
s1.enroll("Math")
s2.enroll("Python")
s3.enroll("Science")

s1.describe()
s2.describe()
s3.describe()

# Modifying class variable affects ALL instances
Student.school_name = "Advanced Python Academy"
print(f"\nAfter renaming school:")
print(f"  s1 school: {s1.school_name}")   # updated
print(f"  s2 school: {s2.school_name}")   # updated too

# WARNING: setting instance attr with same name SHADOWS class variable
s2.school_name = "Private School"   # creates instance variable on s2 only
print(f"\nAfter s2.school_name override:")
print(f"  s1 school: {s1.school_name}")  # still class var
print(f"  s2 school: {s2.school_name}")  # now instance var (shadows class var)
print(f"  Class var: {Student.school_name}")  # class var unchanged


# Practical example: Counter class using class variable
class Counter:
    """Uses a class variable to count instances."""

    count = 0

    def __init__(self):
        Counter.count += 1
        self.id = Counter.count

    @classmethod
    def get_count(cls):
        """Class method to return the count (no instance needed)."""
        return cls.count

    @staticmethod
    def reset():
        """Static method — utility that doesn't need self or cls."""
        Counter.count = 0
        print("Counter reset.")


print("\n--- Counter class ---")
c1 = Counter()
c2 = Counter()
c3 = Counter()
print(f"Total counters: {Counter.get_count()}")  # 3

Counter.reset()
print(f"After reset: {Counter.get_count()}")     # 0
