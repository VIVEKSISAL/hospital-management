# Hospital Management System

A comprehensive, production-ready Hospital Management System built with Python Flask, MySQL, and Bootstrap. This system provides complete management of hospital operations including patient records, doctor profiles, appointments, billing, rooms, and laboratory reports.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-lightblue)
![MySQL](https://img.shields.io/badge/MySQL-5.7+-blue)

## 🎯 Features

### Core Modules

1. **User Authentication & Role Management**
   - Four user roles: Admin, Doctor, Receptionist, Patient
   - Secure login/logout with password hashing (bcrypt)
   - Role-based access control (RBAC)
   - Session management

2. **Patient Management**
   - Add, edit, and delete patient records
   - Store detailed patient information (medical history, allergies, medications)
   - Patient search and filtering
   - Patient history tracking
   - Emergency contact information

3. **Doctor Management**
   - Add and manage doctor profiles
   - Specialization tracking (Cardiology, Orthopedics, etc.)
   - Consultation fees and availability
   - License number verification
   - Experience and qualification management

4. **Appointment System**
   - Book appointments with available time slots
   - Prevent double booking
   - Update appointment status (Scheduled, Completed, Cancelled)
   - Cancel appointments (with date/time validation)
   - View appointment history and upcoming appointments

5. **Billing System**
   - Create detailed bills with multiple cost components
   - Track consultation fees, medicine costs, test costs, room charges
   - Record and manage payments
   - Payment status tracking (Unpaid, Partial, Paid)
   - Discount and billing amount calculation
   - Payment method recording

6. **Room/Ward Management**
   - Manage hospital rooms and wards
   - Room type categorization (General, Semi-Private, Private, ICU)
   - Track occupancy and capacity
   - Allocate rooms to patients
   - Discharge patients from rooms
   - Room availability status

7. **Laboratory/Test Management**
   - Create and manage lab reports
   - Test status tracking (Pending, Complete, Cancelled)
   - Link reports with patients
   - Record test results and normal ranges
   - Doctor-assigned test management

8. **Admin Dashboard**
   - System statistics and analytics
   - Revenue tracking
   - Patient and doctor counts
   - Appointment analytics
   - Room occupancy visualization
   - Quick action buttons

## 💻 Tech Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: MySQL 5.7+
- **ORM**: SQLAlchemy 3.0.5
- **Authentication**: Flask-Login 0.6.2
- **Password Security**: bcrypt 4.0.1
- **Database Connector**: PyMySQL 1.1.0

### Frontend
- **HTML5**: For semantic markup
- **CSS3**: Bootstrap 5.1.3 for responsive design
- **JavaScript**: Vanilla JS for interactivity
- **Icons**: Font Awesome 6.0.0

### Additional Libraries
- WTForms 3.0.1 for form validation
- Python-dateutil 2.8.2 for date handling
- Email-validator 2.0.0 for email validation

## 📋 System Requirements

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- 512MB RAM (minimum)
- 500MB disk space

## 🚀 Quick Start

### 1. Clone or Extract Project
```bash
cd "path/to/pythone hospital management"
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
```bash
# Open MySQL and run:
mysql -u root -p < hospital_management.sql
```

### 5. Update Configuration
Edit `config.py` and update database connection:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/hospital_management'
```

### 6. Run Application
```bash
python app.py
```

### 7. Access in Browser
Open `http://localhost:5000` in your web browser

## 🔐 Demo Credentials

| Role | Username | Password | Features |
|------|----------|----------|----------|
| Admin | admin | password | Full system access, user management, analytics |
| Doctor | dr_sharma | password | Patient appointments, lab reports, prescriptions |
| Patient | patient1 | password | View own records, book appointments, view bills |
| Receptionist | receptionist | password | Patient registration, appointment booking, billing |

## 📁 Project Structure

```
hospital-management-system/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── hospital_management.sql   # Database schema
├── SETUP_GUIDE.md           # Detailed setup instructions
├── README.md                # This file
├── models/                  # SQLAlchemy models
│   ├── user.py
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   ├── billing.py
│   ├── room.py
│   ├── lab_report.py
│   ├── medicine.py
│   └── prescription.py
├── routes/                  # Flask blueprints
│   ├── auth.py
│   ├── dashboard.py
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   ├── billing.py
│   ├── room.py
│   └── lab_report.py
├── templates/               # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   ├── dashboard/
│   ├── patient/
│   ├── doctor/
│   ├── appointment/
│   ├── billing/
│   ├── room/
│   ├── lab_report/
│   └── errors/
├── static/                  # CSS, JS, images
│   ├── css/style.css
│   ├── js/script.js
│   └── img/
└── utils/                   # Utility functions
    └── decorators.py
```

## 🗄️ Database Schema

### Key Tables

| Table | Description |
|-------|-------------|
| users | All system users with roles |
| patients | Patient records and medical info |
| doctors | Doctor info and specializations |
| appointments | Appointment scheduling |
| billing | Patient bills and payments |
| rooms | Hospital rooms/wards |
| room_allocations | Patient room assignments |
| lab_reports | Laboratory test results |
| medicines | Medicine inventory |
| prescriptions | Doctor-prescribed medicines |

## 🔧 Key Features Explained

### Role-Based Access Control
- Admin: Full system access, user management, analytics
- Doctor: Patient management, appointment handling, lab reports
- Receptionist: Patient registration, appointment booking, billing
- Patient: Own records, booking appointments, viewing bills

### Security Features
- Password hashing using bcrypt
- SQL injection protection (SQLAlchemy ORM)
- CSRF protection (Flask-WTF)
- Role-based authorization decorators
- Input validation on forms

### Data Management
- Automatic timestamp tracking (created_at, updated_at)
- Soft delete capability through status fields
- Foreign key relationships for data integrity
- Pagination for list views (10 items per page)

### Search & Filters
- Patient search by name, email, or phone
- Doctor search by name or specialization
- Appointment filtering by status
- Bill filtering by payment status

## 📊 Dashboard Features

### Admin Dashboard
- Total patients, doctors, rooms count
- Today's and upcoming appointments
- Monthly revenue tracking
- Room occupancy statistics
- Recent patient activity

### Doctor Dashboard
- Today's appointment list
- Pending appointments
- Completed appointment count
- Pending lab reports

### Receptionist Dashboard
- Today's appointments count
- New patients registered today
- Available doctors and rooms
- Quick action buttons

### Patient Dashboard
- Upcoming appointments
- Pending bills with amounts
- Lab reports
- Current room allocation (if admitted)

## 🎨 UI/UX Features

- Responsive Bootstrap 5 design
- Mobile-friendly interface
- Color-coded status badges
- Interactive forms with validation
- Toast notifications for actions
- Confirmation dialogs for destructive actions
- Loading spinners for async operations

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

**Issue**: "Access denied for user 'root'@'localhost'"
- Update credentials in config.py
- Ensure MySQL is running

**Issue**: Port 5000 already in use
- Change port in app.py: `app.run(port=5001)`

**Issue**: Template not found
- Ensure templates folder structure matches routes
- Check file names match exactly

See `SETUP_GUIDE.md` for more troubleshooting steps.

## 📈 Performance Optimization

- Database indexing on frequently queried fields
- Pagination implemented on all list views
- Lazy loading for relationships
- Query optimization with selective columns
- Session-based caching for user data

## 🔐 Security Best Practices

1. **Password Security**
   - Bcrypt hashing with salt
   - Minimum 6 character requirement
   - Secure password reset mechanism

2. **Data Protection**
   - Encrypted password storage
   - Role-based access control
   - Input validation and sanitization
   - SQL injection prevention via ORM

3. **Session Management**
   - Secure session cookies
   - Session timeout after 7 days
   - Login required for protected routes

## 🚀 Deployment Guide

### For Production Deployment

1. **Set environment variables:**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key-here
   export DATABASE_URL=mysql+pymysql://user:pass@host/db
   ```

2. **Install production WSGI server:**
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

4. **Configure reverse proxy (Nginx):**
   - Setup SSL/TLS
   - Configure upstream to Gunicorn
   - Enable gzip compression

5. **Database Setup:**
   - Use remote MySQL instance
   - Enable backups
   - Set up replication

## 📝 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - Patient registration
- `GET /auth/logout` - User logout

### Dashboard
- `GET /dashboard/` - Main dashboard
- `GET /dashboard/admin` - Admin dashboard
- `GET /dashboard/doctor` - Doctor dashboard
- `GET /dashboard/receptionist` - Receptionist dashboard

### Patients
- `GET /patients/` - List patients
- `GET /patients/<id>` - View patient details
- `POST /patients/new` - Add new patient
- `POST /patients/<id>/edit` - Edit patient

### Doctors
- `GET /doctors/` - List doctors
- `GET /doctors/<id>` - View doctor details
- `POST /doctors/new` - Add new doctor

### Appointments
- `GET /appointments/` - List appointments
- `POST /appointments/book` - Book appointment
- `POST /appointments/<id>/cancel` - Cancel appointment

### Billing
- `GET /billing/` - List bills
- `POST /billing/new` - Create bill
- `POST /billing/<id>/pay` - Record payment

## 🤝 Contributing

This is a learning project. Feel free to extend and improve!

Suggestions for enhancement:
- Add SMS notifications
- Implement email reminders
- Create mobile app API
- Add advanced analytics
- Implement QR codes for patient IDs

## 📄 License

MIT License - Feel free to use this project for education and commercial purposes.

## 👨‍💻 Author

Hospital Management System v1.0.0
Created: 2026
Updated: March 2026

## 📞 Support

For issues, questions, or contributions:
- Email: info@hospital.com
- Phone: +1-234-567-8900
- Website: www.hospital.com

## ✨ Acknowledgments

- Flask framework and ecosystem
- Bootstrap for responsive UI design
- Font Awesome for icons
- SQLAlchemy for ORM
- The open-source community

---

**Happy coding! Enjoy managing your hospital with this comprehensive system.** 🏥✨
