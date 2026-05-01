# 🏠 Hostel Complaint Management System

A full-stack Django web application for managing hostel complaints.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML + Tailwind CSS (CDN) + JavaScript
- **Database**: SQLite

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install django
```

### 2. Run the server
```bash
cd hostel_project
python manage.py runserver
```

### 3. Open in browser
Visit: http://127.0.0.1:8000

## 👤 Demo Credentials

### Admin Login
- Username: `admin`
- Password: `admin123`

### Student Logins
- Username: `rahul` / Password: `student123`
- Username: `priya` / Password: `student123`

## 📁 Project Structure
```
hostel_project/
├── manage.py
├── db.sqlite3
├── hostel_project/
│   ├── settings.py
│   └── urls.py
└── complaints/
    ├── models.py          # CustomUser + Complaint models
    ├── views.py           # All views (student + admin)
    ├── urls.py            # URL routing
    ├── migrations/
    └── templates/
        ├── base.html          # Shared layout with navbar
        ├── login.html
        ├── register.html
        ├── student_dashboard.html
        ├── submit_complaint.html
        └── admin_dashboard.html
```

## ✨ Features

### Student
- Register / Login
- Submit complaints with title, description, priority
- View all complaints with status badges
- Filter by status, search by title

### Admin
- Custom dashboard (no Django admin panel)
- View all students' complaints
- Sort by Priority (High → Medium → Low) then by latest
- Update complaint status (Pending → In Progress → Resolved)
- Delete complaints
- Filter by priority, status, search

## 🎨 Design
- Dark theme with orange accent
- Syne + DM Sans typography
- Responsive (mobile + desktop)
- Toast notifications
- Color-coded priority badges (Red/Orange/Yellow)
- Color-coded status badges (Gray/Blue/Green)
