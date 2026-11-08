from flask import Flask, jsonify, request
from database import get_db_connection

app = Flask(__name__)


# 1. Home endpoint
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Student Data as a Service",
        "service": "Student Information DaaS",
        "status": "Running"
    })


# 2. Get all students
@app.route("/students", methods=["GET"])
def get_students():

    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# 3. Get student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# 4. Search students
@app.route("/search", methods=["GET"])
def search_students():

    department = request.args.get("department")
    name = request.args.get("name")

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if department:
        query += " AND department = ?"
        params.append(department)

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")

    conn = get_db_connection()

    students = conn.execute(query, params).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# 5. Health check
@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "service": "Student DaaS"
    })


if __name__ == "__main__":
    app.run(debug=True)