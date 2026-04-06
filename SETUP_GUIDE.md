# Hospital Management System - Setup Guide

## Prerequisites

Before you start, ensure you have the following installed on your system:

- **Python 3.8 or higher**: Download from https://www.python.org/
- **MySQL 5.7 or higher**: Download from https://www.mysql.com/
- **Git**: Download from https://git-scm.com/ (optional)
- **pip**: Python package installer (comes with Python)
- **virtualenv**: Python virtual environment tool (install using pip)

## Installation Steps

### Step 1: Set Up MySQL Database

1. **Open MySQL:**
   ```bash
   mysql -u root -p
   ```

2. **Import the database schema:**
   ```bash
   mysql -u root -p < hospital_management.sql
   ```

3. **Verify the database:**
   ```bash
   mysql -u root -p
   USE hospital_management;
   SHOW TABLES;
   EXIT;
   ```

### Step 2: Create Python Virtual Environment

```bash
# Navigate to project directory
cd "path/to/pythone hospital management"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Connection

Edit `config.py` file and update the database connection string:

```python
# Change this line in config.py (line 10)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost/hospital_management'
```

Replace:
- `root` with your MySQL username
- `your_password` with your MySQL password
- `localhost` with your database host (if different)

### Step 5: Run the Application

```bash
python app.py
```

The application should start successfully. You'll see:
```
 * Running on http://127.0.0.1:5000
```

## Access the Application

1. **Open your browser** and go to: `http://localhost:5000`

2. **Login with demo credentials:**

   **Admin Account:**
   - Username: `admin`
   - Password: `password`
   - Role: Admin

   **Doctor Account:**
   - Username: `dr_sharma`
   - Password: `password`
   - Role: Doctor

   **Patient Account:**
   - Username: `patient1`
   - Password: `password`
   - Role: Patient

   **Receptionist Account:**
   - Username: `receptionist`
   - Password: `password`
   - Role: Receptionist

## Project Structure

```
hospital-management-system/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── hospital_management.sql         # Database schema
├── models/                         # Database models
│   ├── __init__.py
│   ├── user.py                     # User model
│   ├── patient.py                  # Patient model
│   ├── doctor.py                   # Doctor model
│   ├── appointment.py              # Appointment model
│   ├── billing.py                  # Billing model
│   ├── room.py                     # Room model
│   ├── room_allocation.py          # Room Allocation model
│   ├── lab_report.py               # Lab Report model
│   ├── medicine.py                 # Medicine model
│   └── prescription.py             # Prescription model
├── routes/                         # Route handlers (blueprints)
│   ├── __init__.py
│   ├── auth.py                     # Authentication routes
│   ├── dashboard.py                # Dashboard routes
│   ├── patient.py                  # Patient routes
│   ├── doctor.py                   # Doctor routes
│   ├── appointment.py              # Appointment routes
│   ├── billing.py                  # Billing routes
│   ├── room.py                     # Room routes
│   └── lab_report.py               # Lab Report routes
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── auth/
│   │   ├── login.html              # Login page
│   │   └── register.html           # Registration page
│   ├── dashboard/                  # Dashboard templates
│   │   ├── admin_dashboard.html
│   │   ├── doctor_dashboard.html
│   │   ├── receptionist_dashboard.html
│   │   └── patient_dashboard.html
│   ├── patient/                    # Patient templates
│   │   ├── list.html               # Patient list
│   │   ├── add.html                # Add patient
│   │   ├── edit.html               # Edit patient
│   │   └── view.html               # View patient details
│   ├── doctor/                     # Doctor templates
│   │   ├── list.html               # Doctor list
│   │   ├── add.html                # Add doctor
│   │   └── view.html               # View doctor details
│   ├── appointment/                # Appointment templates
│   │   ├── list.html               # Appointments list
│   │   ├── book.html               # Book appointment
│   │   ├── edit.html               # Edit appointment
│   │   └── view.html               # View appointment
│   ├── billing/                    # Billing templates
│   │   ├── list.html               # Bills list
│   │   ├── add.html                # Create bill
│   │   ├── view.html               # View bill
│   │   ├── edit.html               # Edit bill
│   │   └── pay.html                # Record payment
│   ├── room/                       # Room templates
│   │   ├── list.html               # Rooms list
│   │   ├── add.html                # Add room
│   │   ├── view.html               # View room
│   │   ├── edit.html               # Edit room
│   │   └── allocate.html           # Allocate room
│   ├── lab_report/                 # Lab Report templates
│   │   ├── list.html               # Reports list
│   │   ├── add.html                # Add report
│   │   ├── edit.html               # Edit report
│   │   └── view.html               # View report
│   └── errors/
│       ├── 403.html                # Access denied
│       ├── 404.html                # Not found
│       └── 500.html                # Server error
├── static/                         # Static files
│   ├── css/
│   │   └── style.css               # Custom CSS
│   ├── js/
│   │   └── script.js               # Custom JavaScript
│   └── img/                        # Images (if needed)
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── decorators.py               # Custom decorators
└── venv/                           # Virtual environment (created locally)
```

## Features

### 1. User Authentication & Roles
- Secure login/logout system
- Four user roles: Admin, Doctor, Receptionist, Patient
- Password hashing with bcrypt
- Session management

### 2. Patient Management
- Add/edit/delete patient records
- Store medical history, allergies, current medications
- View patient details
- Search functionality

### 3. Doctor Management
- Add/edit doctor profiles
- Specialization tracking
- Consultation fees and availability
- License number management

### 4. Appointment System
- Book appointments
- Prevent double booking
- Update appointment status
- Cancel appointments
- View appointment history

### 5. Billing System
- Create bills with detailed breakdowns
- Track payments
- Payment status management
- Record partial payments
- Billing history

### 6. Room Management
- Manage rooms/wards
- Track occupancy
- Allocate rooms to patients
- Discharge patients
- Room availability status

### 7. Laboratory/Test Management
- Create lab reports
- Track test status
- Record test results
- Link reports with patients

### 8. Admin Dashboard
- System statistics
- Revenue tracking
- Patient/doctor counts
- Appointment analytics
- Room occupancy status

## Database Schema

### Tables
- **users**: All system users
- **patients**: Patient information
- **doctors**: Doctor information
- **appointments**: Appointment records
- **billing**: Bill records
- **rooms**: Room/ward information
- **room_allocations**: Patient room assignments
- **lab_reports**: Laboratory test reports
- **medicines**: Medicine inventory
- **prescriptions**: Medicine prescriptions

## Troubleshooting

### Issue: Database connection failed
**Solution**: Check MySQL is running and verify credentials in `config.py`

### Issue: Import errors
**Solution**: Ensure all requirements are installed: `pip install -r requirements.txt`

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py` (line: `app.run(port=5001, ...)`)

### Issue: bcrypt errors on Windows
**Solution**: Install Visual C++ Build Tools or use: `pip install python-multipart`

### Issue: Templates not found
**Solution**: Ensure `templates/` directory exists in project root

## Creating Additional Templates

To create templates for other features (patient/patient/, doctor/list.html, etc.):

1. Create the directory if it doesn't exist
2. Create `.html` file with the following structure:

```html
{% extends "base.html" %}

{% block title %}Page Title - Hospital Management System{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Your content here -->
</div>
{% endblock %}
```

## Performance Optimization

1. **Database Indexing**: Already included in SQL file
2. **Pagination**: Implemented in list views (10 items per page)
3. **Caching**: Use Flask-Caching for frequently accessed data
4. **Query Optimization**: Use eager loading for relationships

## Security Best Practices

1. **Password Security**: Using bcrypt hashing
2. **SQL Injection**: Using SQLAlchemy ORM
3. **CSRF Protection**: Flask-WTF enabled
4. **Input Validation**: Server-side and client-side validation
5. **Role-based Access**: Custom decorators for authorization

## Deployment

To deploy to production:

1. Set `FLASK_ENV=production` in environment
2. Use a WSGI server (Gunicorn, uWSGI)
3. Enable HTTPS
4. Set strong `SECRET_KEY` in config
5. Use environment variables for sensitive data

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

## Support & Maintenance

For updates or issues:
1. Check error logs
2. Review database connectivity
3. Verify all dependencies are installed
4. Check Flask debug mode logs

## Future Enhancements

- SMS notifications for appointments
- Email reminders
- Insurance management
- Pharmacy integration
- Mobile app API
- Advanced analytics
- Multi-language support
- Video consultation

## License

Hospital Management System © 2026. All rights reserved.

## Contact

For support or inquiries:
- Email: info@hospital.com
- Phone: +1-234-567-8900
- Website: www.hospital.com

---

**Enjoy using the Hospital Management System!**
