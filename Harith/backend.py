# ==============================
# IMPORT LIBRARIES
# ==============================
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os  # FIX: added for absolute database path

# ==============================
# CREATE FLASK APP
# ==============================
app = Flask(__name__)
CORS(app)

# ==============================
# SQLITE CONFIGURATION
# ==============================

# FIX: get absolute path of current folder (Harith folder)
basedir = os.path.abspath(os.path.dirname(__file__))

print("DATABASE PATH:", os.path.join(basedir, "database.db"))

# FIX: ensures database.db is always correctly linked
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================
# DATABASE MODELS (FIXED VERSION)
# ==============================

# ------------------------------
# COURSEWORK TABLE (PARENT)
# ------------------------------
class Coursework(db.Model):
    __tablename__ = "coursework"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    
    # FIX: use proper DATE type instead of string
    due_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), default="Pending")

    # RELATIONSHIP: one coursework has many members
    members = db.relationship('Member', backref='coursework', lazy=True)


# ------------------------------
# MEMBER TABLE (CHILD)
# ------------------------------
class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(db.String(50))

    # FIX: proper foreign key relationship
    coursework_id = db.Column(db.Integer, db.ForeignKey('coursework.id'))


# ==============================
# CREATE DATABASE (RUN ONCE ONLY)
# ==============================
# IMPORTANT:
# Run this ONCE manually or via separate init script, then comment it back.

# with app.app_context():
#     db.create_all()


# ==============================
# HOME ROUTE
# ==============================
@app.route("/")
def home():
    return "Flowly Backend with Proper SQLite Running 🚀"


# ==============================
# ADD MEMBER
# ==============================
@app.route("/add_member", methods=["POST"])
def add_member():
    data = request.get_json()  # FIX: safer than request.json

    if not data or "name" not in data:
        return jsonify({"error": "Invalid input"}), 400

    member = Member(
        name=data["name"],
        email=data.get("email", ""),
        role=data.get("role", ""),
        coursework_id=data.get("coursework_id")
    )

    db.session.add(member)
    db.session.commit()

    return jsonify({"message": "Member added successfully"})


# ==============================
# GET ALL MEMBERS
# ==============================
@app.route("/all_members", methods=["GET"])
def all_members():
    members = Member.query.all()

    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "email": m.email,
            "role": m.role,
            "coursework_id": m.coursework_id
        }
        for m in members
    ])

# ==============================
# REGISTER ROUTE
# ==============================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "Missing fields"
        })

    # TEMP LOGIC (no database storage yet)
    return jsonify({
        "success": True,
        "message": "User registered successfully"
    })

# ==============================
# ADD COURSEWORK
# ==============================
@app.route("/add_coursework", methods=["POST"])
def add_coursework():

    # DEBUG: raw incoming request
    print("RAW DATA:", request.data)

    # FIX: force JSON parsing (important for your issue)
    data = request.get_json(force=True)

    print("DATA RECEIVED:", data)  # ✅ DEBUG CHECKPOINT

    if not data or "title" not in data or "due_date" not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Convert string → date object
    due_date_obj = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    task = Coursework(
        title=data["title"],
        description=data.get("description", ""),
        due_date=due_date_obj,
        status="Pending"
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Coursework added successfully"})

# ==============================
# DELETE COURSEWORK
# ==============================
@app.route("/delete_coursework/<int:id>", methods=["DELETE"])
def delete_coursework(id):
    task = Coursework.query.get(id)

    if not task:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})

# ==============================
# GET ALL COURSEWORK (WITH DAYS LEFT)
# ==============================
@app.route("/upcoming", methods=["GET"])
def upcoming():
    tasks = Coursework.query.all()
    today = datetime.now().date()

    result = []

    for t in tasks:
        days_left = (t.due_date - today).days

        if days_left >= 0:
            result.append({
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "due_date": t.due_date.strftime("%Y-%m-%d"),
                "days_left": days_left,
                "status": "URGENT ⚠️" if days_left <= 3 else "NORMAL"
            })

    result.sort(key=lambda x: x["days_left"])
    return jsonify(result)


# ==============================
# URGENT ALERTS (0–3 DAYS)
# ==============================
@app.route("/alerts", methods=["GET"])
def alerts():
    tasks = Coursework.query.all()
    today = datetime.now().date()

    result = []

    for t in tasks:
        days_left = (t.due_date - today).days

        if 0 <= days_left <= 3:
            result.append({
                "id": t.id,
                "title": t.title,
                "days_left": days_left,
                "status": "URGENT ⚠️"
            })

    return jsonify(result)


# ==============================
# OVERDUE TASKS
# ==============================
@app.route("/overdue", methods=["GET"])
def overdue():
    tasks = Coursework.query.all()
    today = datetime.now().date()

    result = []

    for t in tasks:
        days_left = (t.due_date - today).days

        if days_left < 0:
            result.append({
                "id": t.id,
                "title": t.title,
                "due_date": t.due_date.strftime("%Y-%m-%d"),
                "status": "OVERDUE ❌"
            })

    return jsonify(result)

# ==============================
# LOGIN (ADDED ONLY)
# ==============================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # TEMP LOGIC (no database auth yet)
    if email and password:
        return jsonify({
            "success": True,
            "message": "Login successful"
        })

    return jsonify({
        "success": False,
        "message": "Invalid email or password"
    })

# ==============================
# FORGOT PASSWORD (ADDED ONLY)
# ==============================
@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()

    email = data.get("email")

    # TEMP LOGIC (upgrade later with real DB check)
    if email:
        return jsonify({
            "success": True,
            "message": "Reset link sent"
        })

    return jsonify({
        "success": False,
        "message": "Invalid email"
    })




@app.route("/debug_db", methods=["GET"])
def debug_db():
    tasks = Coursework.query.all()
    return jsonify([
        {"id": t.id, "title": t.title}
        for t in tasks
    ])
# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    app.run(debug=True)