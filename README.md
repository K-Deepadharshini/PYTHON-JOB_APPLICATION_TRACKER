📂 Job Application Tracker
The Job Application Tracker is a full-stack web application that allows users to manage and monitor their job search process — from submitting applications to tracking interviews, updating statuses, and storing interview tips. Ideal for students, job seekers, and professionals.

🚀 Features
🔎 Add/View Applications: Submit and browse job applications with complete details.

🏢 Company Management: Store and manage company information including name, location, email, and contact number.

📅 Interview Tracking: Schedule and view interviews with outcomes.

🔄 Status Updates: Track application progress (Applied, Interview Scheduled, Offer Received, Rejected).

🧠 Interview Tips: Helpful interview preparation tips and guidance section.

🧾 Summary Page: A consolidated overview of all job applications and statuses.

🗓 Calendar Notes: Mark interview dates, deadlines, or notes on a calendar interface.

👤 Authentication: Login and signup system for secure access.

🔐 Logout: Secure logout functionality.

💡 About Section: Know more about the app’s purpose and creators.

🎯 User-Friendly UI: Clean interface for smooth navigation and accessibility.

🛠 Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Database: MySQL (phpMyAdmin)

IDE: VSCode

📁 Folder Structure
JOB_TRACKER_COMPLETE/
├── _pycache_/
├── templates/
│   ├── add.html                 # Form to add new applications
│   ├── auth.html                # Login/signup interface
│   ├── index.html               # Homepage/dashboard
│   ├── interviews.html          # Interview scheduling & tracking
│   ├── update.html              # Update application status/details
│   ├── view.html                # View all job applications
│   ├── tips.html                # Interview tips page
│   ├── about.html               # About the application
│   ├── calendar.html            # Calendar to mark notes
│   ├── summary.html             # Overall application summary
├── venv/                        # Python virtual environment
├── app.py                       # Main Flask backend app
├── job_tracker_schema.sql       # SQL schema for MySQL database
├── requirements.txt             # Python dependencies
├── test_flask.py                # Unit tests for Flask routes
├── test_phpmyadmin_connect.py   # Test for DB connection
🧾 Database Tables
users:
Stores user login and authentication details.
Fields: user_id, username, email, password_hash, created_at

applications:
Stores job application details submitted by users.
Fields: application_id, user_id, company_id, job_title, application_date, notes, current_status

companies:
Stores company-related data.
Fields: company_id, company_name, location, email, phone

interviews:
Holds interview schedules and outcomes linked to applications.
Fields: interview_id, application_id, interview_date, interview_mode, outcome, notes

status_updates:
Tracks the status history of each job application over time.
Fields: update_id, application_id, status, updated_at, remarks
📌 Future Enhancements
📧 Email reminders for interviews and deadlines

📂 Resume upload and file management

📊 Application insights dashboard with charts



Developed by Anushri T and Deepadharshini K
