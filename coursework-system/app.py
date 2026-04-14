from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coursework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            due_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coursework")
    coursework_list = cursor.fetchall()
    conn.close()

    return render_template('index.html', coursework_list=coursework_list)

@app.route('/add', methods=['POST'])
def add_coursework():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO coursework (title, description, due_date) VALUES (?, ?, ?)",
        (title, description, due_date)
    )
    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/delete/<int:id>')
def delete_coursework(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM coursework WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit_coursework(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coursework WHERE id = ?", (id,))
    coursework = cursor.fetchone()
    conn.close()

    return render_template('edit.html', coursework=coursework)

@app.route('/update/<int:id>', methods=['POST'])
def update_coursework(id):
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE coursework
        SET title = ?, description = ?, due_date = ?
        WHERE id = ?
    """, (title, description, due_date, id))
    conn.commit()
    conn.close()

    return redirect('/')
if __name__ == '__main__':
    init_db()
    app.run(debug=True)