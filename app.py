from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('vacancies.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY,
            school_name TEXT,
            month TEXT,
            teacher_vacancies INTEGER,
            nonteaching_vacancies INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    school_name = request.form['school_name']
    month = request.form['month']
    teacher_vacancies = int(request.form['teacher_vacancies'])
    nonteaching_vacancies = int(request.form['nonteaching_vacancies'])

    conn = sqlite3.connect('vacancies.db')
    c = conn.cursor()
    c.execute("INSERT INTO vacancies (school_name, month, teacher_vacancies, nonteaching_vacancies) VALUES (?, ?, ?, ?)",
              (school_name, month, teacher_vacancies, nonteaching_vacancies))
    conn.commit()
    conn.close()
    return render_template('submitted.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

from flask import session, url_for

# Add secret key at the top of app.py
app.secret_key = 'your_secret_key_here'

# Dummy admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin.html', error="Invalid credentials")
    return render_template('admin.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    # Example content for the admin dashboard
    conn = sqlite3.connect('vacancies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vacancies")
    data = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', vacancies=data)