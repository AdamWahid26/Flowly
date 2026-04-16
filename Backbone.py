# ==============================
# IMPORT LIBRARIES
# ==============================
from flask import Flask, request, jsonify
from datetime import datetime


# ==============================
# CREATE FLASK APP
# ==============================
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app = Flask(__name__)

# ==============================
# TEMPORARY "DATABASE"
# ==============================
# Store group members in memory
group_members = []

# Store coursework in memory
courseworks = [
    {"id": 1, "title": "Math Assignment", "due_date": "2026-04-20"},
    {"id": 2, "title": "English Essay", "due_date": "2026-04-18"},
    {"id": 3, "title": "Science Project", "due_date": "2026-04-25"}
]

# ==============================
# HOME ROUTE (CHECK SERVER)
# ==============================
@app.route("/")
def home():
    return "Flowly Backend is Running 🚀"


# ==============================
# ADD GROUP MEMBER
# ==============================
@app.route("/add_member", methods=["POST"])
def add_member():
    # Get data from frontend (JSON)
    data = request.json

    # Create member object
    member = {
        "name": data["name"],
        "email": data["email"],
        "role": data["role"],
        "coursework_id": data["coursework_id"]  # link to coursework
    }

    # Save into memory list
    group_members.append(member)

    # Return success message
    return jsonify({"message": "Member added successfully"})


# ==============================
# ADD COURSEWORK
# ==============================
@app.route("/add_coursework", methods=["POST"])
def add_coursework():
    data = request.json

    # Create new coursework object
    new_task = {
        "id": len(courseworks) + 1,
        "title": data["title"],
        "due_date": data["due_date"]
    }

    # Save into list
    courseworks.append(new_task)

    return jsonify({"message": "Coursework added successfully"})


# ==============================
# GET MEMBERS BY COURSEWORK
# ==============================
@app.route("/members/<int:coursework_id>", methods=["GET"])
def get_members(coursework_id):

    # Filter members by coursework ID
    filtered = []

    for m in group_members:
        if m["coursework_id"] == coursework_id:
            filtered.append(m)

    return jsonify(filtered)


# ==============================
# GET ALL MEMBERS
# ==============================
@app.route("/all_members", methods=["GET"])
def all_members():
    return jsonify(group_members)


# ==============================
# UPCOMING COURSEWORK
# ==============================
@app.route("/upcoming", methods=["GET"])
def upcoming():

    today = datetime.now().date()
    result = []

    # Loop through coursework list
    for c in courseworks:

        # Convert string date → date object
        due_date = datetime.strptime(c["due_date"], "%Y-%m-%d").date()

        # Calculate days left
        days_left = (due_date - today).days

        # Only future tasks
        if days_left >= 0:
            item = c.copy()
            item["days_left"] = days_left
            result.append(item)

    # Sort by nearest deadline
    result.sort(key=lambda x: x["days_left"])

    return jsonify(result)


# ==============================
# ALERTS (URGENT TASKS)
# ==============================
@app.route("/alerts", methods=["GET"])
def alerts():

    today = datetime.now().date()
    alerts_list = []

    for c in courseworks:
        due_date = datetime.strptime(c["due_date"], "%Y-%m-%d").date()
        days_left = (due_date - today).days

        # Only tasks within 3 days
        if 0 <= days_left <= 3:
            item = c.copy()
            item["days_left"] = days_left
            item["status"] = "URGENT ⚠️"
            alerts_list.append(item)

    return jsonify(alerts_list)


# ==============================
# OVERDUE TASKS
# ==============================
@app.route("/overdue", methods=["GET"])
def overdue():

    today = datetime.now().date()
    overdue_list = []

    for c in courseworks:
        due_date = datetime.strptime(c["due_date"], "%Y-%m-%d").date()
        days_left = (due_date - today).days

        # Past deadline
        if days_left < 0:
            item = c.copy()
            item["status"] = "OVERDUE ❌"
            overdue_list.append(item)

    return jsonify(overdue_list)


# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    app.run(debug=True)