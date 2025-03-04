from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS meetings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  start_time DATETIME NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        title = request.form['title']
        start_time = request.form['start_time']
        
        # Save meeting to database
        conn = sqlite3.connect('meetings.db')
        c = conn.cursor()
        c.execute("INSERT INTO meetings (title, start_time) VALUES (?, ?)",
                  (title, start_time))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('schedule.html')

@app.route('/meeting/<int:meeting_id>')
def meeting(meeting_id):
    return render_template('meeting.html', meeting_id=meeting_id)

if __name__ == '__main__':
    app.run(debug=True)