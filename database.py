import sqlite3

def get_db_connection():
    conn = sqlite3.connect("students.db")

    # Return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row

    return conn


def get_all_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return students


if __name__ == "__main__":

    students = get_all_students()

    print("Total Students:", len(students))

    for student in students:
        print(dict(student))