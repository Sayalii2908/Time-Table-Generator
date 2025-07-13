import sqlite3

conn = sqlite3.connect('timetable.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS subjects")
cursor.execute("DROP TABLE IF EXISTS teachers")

cursor.execute("""
    CREATE TABLE subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        year TEXT NOT NULL CHECK(year IN ('FY', 'SY'))
    )
""")

cursor.execute("""
    CREATE TABLE teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject_id INTEGER,
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )
""")

# Subjects for FY and SY
subjects = [
    ("CS101", "Data Structures", "FY"),
    ("CS102", "C Programming", "FY"),
    ("CS103", "Python Programming", "FY"),
    ("CS104", "Computer Organization", "FY"),
    ("CS201", "DBMS", "SY"),
    ("CS202", "Computer Networks", "SY"),
    ("CS203", "Web Technologies", "SY"),
    ("CS204", "Operating Systems", "SY")
]
cursor.executemany("INSERT INTO subjects (code, name, year) VALUES (?, ?, ?)", subjects)

# Assign the same teachers to multiple subjects
teachers = [
    ("Prof. Sharma", 1),  # CS101
    ("Ms. Mehta", 2),     # CS102
    ("Prof. Sharma", 3),  # CS103
    ("Ms. Mehta", 4),     # CS104
    ("Prof. Sharma", 5),  # CS201
    ("Ms. Mehta", 6),     # CS202
    ("Prof. Sharma", 7),  # CS203
    ("Ms. Mehta", 8)      # CS204
]
cursor.executemany("INSERT INTO teachers (name, subject_id) VALUES (?, ?)", teachers)

conn.commit()
conn.close()
print("Database updated with 8 subjects and shared teachers.")

