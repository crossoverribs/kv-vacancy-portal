from flask import Flask, render_template, request, redirect
import sqlite3

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
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)