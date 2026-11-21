"""Attendly - simple student attendance tracker using Python only."""

from datetime import date, datetime
from pathlib import Path
import json


# Demo teacher login
TEACHER_USERNAME = "teacher"
TEACHER_PASSWORD = "teach123"

# Attendance data is saved beside this Python file
DATA_FILE = Path(__file__).with_name("attendance_data.json")

# Sample class
STUDENTS = [
    {"id": "STU-101", "name": "Aarav Sharma"},
    {"id": "STU-102", "name": "Mira Patel"},
    {"id": "STU-103", "name": "Kabir Singh"},
    {"id": "STU-104", "name": "Ananya Rao"},
    {"id": "STU-105", "name": "Dev Mehta"},
    {"id": "STU-106", "name": "Isha Kapoor"},
    {"id": "STU-107", "name": "Rohan Das"},
    {"id": "STU-108", "name": "Sana Khan"},
    {"id": "STU-109", "name": "Vihaan Joshi"},
    {"id": "STU-110", "name": "Nisha Verma"},
]

STATUSES = {
    "P": "Present",
    "A": "Absent",
    "L": "Late",
    "N": "Not marked",
}


def load_attendance():
    """Load saved attendance from the JSON file."""
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_attendance(records):
    """Save attendance to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def teacher_login():
    """Allow the teacher to sign in."""
    print("=== Attendly Teacher Login ===")

    for attempt in range(3):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username == TEACHER_USERNAME and password == TEACHER_PASSWORD:
            print("\nLogin successful. Welcome, teacher!\n")
            return True

        remaining = 2 - attempt
        if remaining:
            print(f"Incorrect login. Attempts remaining: {remaining}\n")

    print("Too many incorrect attempts.")
    return False


def ask_date():
    """Ask for a date, using today's date when the input is blank."""
    today = date.today().isoformat()
    value = input(f"Attendance date (YYYY-MM-DD) or Enter for {today}: ").strip()

    if not value:
        return today

    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        print("Invalid date. Today's date will be used.")
        return today


def mark_attendance(records):
    """Mark and save attendance for one date."""
    selected_date = ask_date()
    day_records = records.get(selected_date, {})

    print(f"\nMark attendance for {selected_date}")
    print("Enter P = Present, A = Absent, L = Late, N = Not marked\n")

    for student in STUDENTS:
        student_id = student["id"]
        old_status = day_records.get(student_id, "Not marked")

        choice = input(
            f"{student['name']} ({student_id}) "
            f"[current: {old_status}] - status: "
        ).strip().upper()

        if choice in STATUSES:
            day_records[student_id] = STATUSES[choice]
        else:
            print("Invalid choice. Keeping the current status.")
            day_records.setdefault(student_id, old_status)

    records[selected_date] = day_records

    try:
        save_attendance(records)
        print("\nAttendance saved successfully.\n")
    except OSError:
        print("\nCould not save the attendance file. Check folder permissions.\n")


def show_report(records):
    """Show the student list and attendance summary for one date."""
    selected_date = ask_date()
    day_records = records.get(selected_date, {})

    present = sum(value == "Present" for value in day_records.values())
    absent = sum(value == "Absent" for value in day_records.values())
    late = sum(value == "Late" for value in day_records.values())
    not_marked = len(STUDENTS) - present - absent - late

    marked = present + absent + late
    if marked:
        rate = round((present + late) * 100 / marked)
    else:
        rate = 0

    print(f"\n=== Attendance Report: {selected_date} ===")
    print(f"{'Student':<20} {'Student ID':<12} Status")
    print("-" * 52)

    for student in STUDENTS:
        status = day_records.get(student["id"], "Not marked")
        print(f"{student['name']:<20} {student['id']:<12} {status}")

    print("-" * 52)
    print(f"Total students : {len(STUDENTS)}")
    print(f"Present        : {present}")
    print(f"Absent         : {absent}")
    print(f"Late           : {late}")
    print(f"Not marked     : {not_marked}")
    print(f"Attendance rate: {rate}%\n")


def main():
    """Run the Attendly menu."""
    if not teacher_login():
        return

    records = load_attendance()

    while True:
        print("=== Attendly Menu ===")
        print("1. Mark attendance")
        print("2. View attendance report")
        print("3. Exit")

        choice = input("Choose an option: ").strip()
        print()

        if choice == "1":
            mark_attendance(records)
        elif choice == "2":
            show_report(records)
        elif choice == "3":
            print("Thank you for using Attendly. Goodbye!")
            break
        else:
            print("Please choose 1, 2, or 3.\n")


if __name__ == "__main__":
    main()