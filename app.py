import os
import traceback
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash  # ✅ This line is required
import pymysql
from flask_cors import CORS
import pymysql
from flask import request, redirect

app = Flask(__name__)
app.secret_key = 'trackback_secret_2025'
CORS(app)
marked_dates = set()

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'job'
}

def get_db():
    return pymysql.connect(**db_config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=%s", (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row and check_password_hash(row[0], password_input):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"
    return render_template('auth.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return "Username already exists. Try another."

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('auth.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tips')
def tips():
    return render_template('interview_tips.html')
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            data = request.form

            conn = get_db()
            cur = conn.cursor()

            # Check if company already exists
            cur.execute("SELECT company_id FROM companies WHERE company_name = %s", (data['company_name'],))
            company = cur.fetchone()

            if company:
                company_id = company[0]
            else:
                cur.execute(""" 
                    INSERT INTO companies (company_name, company_location, company_email, company_pno)
                    VALUES (%s, %s, %s, %s)
                """, (data['company_name'], data['company_location'], data['company_email'], data['company_pno']))
                company_id = cur.lastrowid

            # Get status_id
            cur.execute("SELECT status_id FROM statuses WHERE status_name = %s", (data['status'],))
            status = cur.fetchone()
            if not status:
                return "Invalid status selected", 400
            status_id = status[0]

            # Insert application
            cur.execute(""" 
                INSERT INTO applications (company_id, job_position, application_date, job_description, status_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (company_id, data['job_position'], data['application_date'], data['job_description'], status_id))

            conn.commit()
            cur.close()
            conn.close()

            return render_template('add.html', success=True)

        except Exception as e:
            traceback.print_exc()
            return f"Error occurred: {str(e)}", 500

    return render_template('add.html')


@app.route('/view', methods=['GET'])
def view_applications():
    if request.args.get('json') == '1':
        conn = get_db()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(""" 
            SELECT a.application_id, c.company_name, a.job_position, a.application_date, 
                   s.status_name AS status, i.interview_date, i.interview_time, i.interview_location
            FROM applications a
            JOIN companies c ON a.company_id = c.company_id
            JOIN statuses s ON a.status_id = s.status_id
            LEFT JOIN interviews i ON a.application_id = i.application_id
            ORDER BY a.application_date DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(result)

    return render_template('view.html')


@app.route('/update', methods=['GET', 'POST'])
def update_application():
    if request.method == 'POST':
        try:
            data = request.form
            application_id = data['application_id']
            status_id = data['status_id']

            conn = get_db()
            cur = conn.cursor()

            # Validate status ID
            cur.execute("SELECT status_id FROM statuses WHERE status_id = %s", (status_id,))
            if not cur.fetchone():
                return render_template('update.html', error="Invalid status ID.")

            # Update application status
            cur.execute("UPDATE applications SET status_id = %s WHERE application_id = %s", (status_id, application_id))
            conn.commit()
            cur.close()
            conn.close()

            return render_template('update.html', success="Application updated successfully!")

        except Exception as e:
            traceback.print_exc()
            return render_template('update.html', error="Error updating application.")

    return render_template('update.html')


@app.route('/delete', methods=['POST'])
def delete_application():
    app_id = request.form.get('application_id')
    if not app_id:
        return "Missing application ID", 400

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='job_tracker'
    )
    cursor = conn.cursor()

    # First delete from dependent table
    cursor.execute("DELETE FROM interviews WHERE application_id = %s", (app_id,))
    # Then delete the main application
    cursor.execute("DELETE FROM applications WHERE application_id = %s", (app_id,))

    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/summary')
def summary():
    conn = get_db()
    cur = conn.cursor()

    # Total applications
    cur.execute("SELECT COUNT(*) FROM applications")
    total_applications = cur.fetchone()[0]

    # Total interviews
    cur.execute("SELECT COUNT(*) FROM interviews")
    total_interviews = cur.fetchone()[0]

    # Show all statuses even if count = 0
    cur.execute("""
        SELECT s.status_name, COUNT(a.application_id) AS count
        FROM statuses s
        LEFT JOIN applications a ON s.status_id = a.status_id
        GROUP BY s.status_name
    """)
    status_counts = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('summary.html',
                           total_applications=total_applications,
                           total_interviews=total_interviews,
                           status_counts=status_counts)


@app.route('/interviews', methods=['GET', 'POST'])
def interviews():
    if request.method == 'POST':
        try:
            data = request.form
            conn = get_db()
            cur = conn.cursor()

            # Get the latest application ID for the company
            cur.execute(""" 
                SELECT a.application_id FROM applications a
                JOIN companies c ON a.company_id = c.company_id
                WHERE c.company_name = %s
                ORDER BY a.application_date DESC LIMIT 1
            """, (data['company'],))
            app_id = cur.fetchone()

            if app_id:
                # Check if an interview already exists for this application
                cur.execute("""
                    SELECT * FROM interviews WHERE application_id = %s
                """, (app_id[0],))
                existing_interview = cur.fetchone()

                if existing_interview:
                    # Update the existing interview
                    cur.execute("""
                        UPDATE interviews 
                        SET interview_date = %s, interview_time = %s, interview_location = %s
                        WHERE application_id = %s
                    """, (data['interview-date'], data['interview-time'], data['interview-location'], app_id[0]))
                else:
                    # Insert a new interview if it doesn't exist
                    cur.execute(""" 
                        INSERT INTO interviews (application_id, interview_date, interview_time, interview_location)
                        VALUES (%s, %s, %s, %s)
                    """, (app_id[0], data['interview-date'], data['interview-time'], data['interview-location']))

                conn.commit()

            cur.close()
            conn.close()

            return redirect(url_for('home'))

        except Exception as e:
            traceback.print_exc()
            return f"Error scheduling or updating interview: {str(e)}", 500

    return render_template('interviews.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', marked=marked_dates)

@app.route('/toggle', methods=['POST'])
def toggle():
    date = request.json.get('date')
    if date in marked_dates:
        marked_dates.remove(date)
        status = "unmarked"
    else:
        marked_dates.add(date)
        status = "marked"
    return jsonify({"status": status, "date": date})

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/test_db')
def test_db():
    try:
        conn = get_db()
        conn.close()
        return "✅ Database connected successfully!", 200
    except pymysql.MySQLError as err:
        return f"❌ Error: {err}", 500


if __name__ == '__main__':
    app.run(debug=True, port=5050)
