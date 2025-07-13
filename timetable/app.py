from flask import Flask, render_template, request
import sqlite3, random

app = Flask(__name__)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
slots = ["9:00-11:00", "11:00-1:00", "2:00-4:00", "4:00-6:00"]

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        room_count_raw = request.form.get("rooms")
        if not room_count_raw or not room_count_raw.isdigit():
            return "❌ Invalid room count. Please go back and try again."

        room_count = int(room_count_raw)
        rooms = [f"R{i+1}" for i in range(room_count)]

        # Load subjects and teachers from DB
        conn = sqlite3.connect('timetable.db')
        c = conn.cursor()
        c.execute("""
            SELECT s.code, s.name, s.year, t.name 
            FROM subjects s 
            JOIN teachers t ON s.id = t.subject_id
        """)
        subjects = c.fetchall()
        conn.close()

        # Initialize timetable
        timetable = {
            'FY': {day: {slot: None for slot in slots} for day in days},
            'SY': {day: {slot: None for slot in slots} for day in days}
        }

        # Track teacher and room availability
        teacher_schedule = {teacher: {day: [] for day in days} for _, _, _, teacher in subjects}
        room_schedule = {room: {day: [] for day in days} for room in rooms}

        # Allocate 2 lectures per subject
        for code, name, year, teacher in subjects:
            assigned = 0
            attempts = 0
            while assigned < 2 and attempts < 500:
                d = random.choice(days)
                s = random.choice(slots)
                r = random.choice(rooms)

                # Check constraints:
                if (
                    timetable[year][d][s] is None and
                    s not in teacher_schedule[teacher][d] and
                    s not in room_schedule[r][d] and
                    len(teacher_schedule[teacher][d]) < 2  # 👈 Only 2 lectures per teacher per day
                ):
                    timetable[year][d][s] = {
                        'code': code,
                        'subject': name,
                        'teacher': teacher,
                        'room': r
                    }
                    teacher_schedule[teacher][d].append(s)
                    room_schedule[r][d].append(s)
                    assigned += 1
                attempts += 1

        return render_template('index.html', timetable=timetable, days=days, slots=slots, rooms=room_count)

    return render_template('form.html')

if __name__ == '__main__':
    print("✅ Flask server is starting on http://127.0.0.1:5000/")
    app.run(debug=True)

