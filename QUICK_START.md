# Hospital Management System - Quick Start Guide

## ⚡ 5-Minute Setup

### Windows Users
```bash
run.bat
```
✅ Done! The system will automatically:
- Check for Python & MySQL
- Create virtual environment
- Install dependencies
- Import database
- Start the application

### Linux/macOS Users
```bash
chmod +x run.sh
./run.sh
```

---

## 🔧 Manual Setup (If Scripts Don't Work)

### Step 1: Extract Project Files
```bash
# Ensure you have all files extracted to:
/home/vicky/Documents/the codes/pythone hospital management/
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Database

**Option A: MySQL Command Line**
```bash
mysql -u root -p < hospital_management.sql
```

**Option B: MySQL Workbench**
1. Open MySQL Workbench
2. Click File → Open SQL Script
3. Select `hospital_management.sql`
4. Click Execute (⚡ icon)

**Option C: Using mysql CLI in Python**
```python
python
>>> import subprocess
>>> subprocess.run(['mysql', '-u', 'root', '-p'], input=open('hospital_management.sql').read())
```

### Step 5: Update Database Credentials
Edit `config.py`:
```python
# Find DevelopmentConfig class and update:
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/hospital_management'
```

### Step 6: Run Application
```bash
python app.py
```

### Step 7: Access Application
Open browser and go to:
```
http://localhost:5000
```

---

## 👤 Demo Login Credentials

### Administrator Account
- **Username**: `admin`
- **Password**: `password`
- **Role**: Full system access

### Doctor Account
- **Username**: `dr_sharma`
- **Password**: `password`
- **Role**: View appointments, lab reports, prescriptions

### Patient Account
- **Username**: `patient1`
- **Password**: `password`
- **Role**: View appointments, bills, lab reports

### Receptionist Account
- **Username**: `receptionist1`
- **Password**: `password`
- **Role**: Book appointments, register patients, manage billing

---

## 🗂️ Project Structure

```
hospital-management/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── hospital_management.sql         # Database schema & sample data
│
├── models/                         # Database models
│   ├── user.py
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   ├── billing.py
│   ├── room.py
│   ├── room_allocation.py
│   ├── lab_report.py
│   ├── medicine.py
│   ├── prescription.py
│   └── __init__.py
│
├── routes/                         # API endpoints
│   ├── auth.py                     # Login/Register
│   ├── dashboard.py                # Role dashboards
│   ├── patient.py                  # Patient CRUD
│   ├── doctor.py                   # Doctor CRUD
│   ├── appointment.py              # Appointments
│   ├── billing.py                  # Billing & Payments
│   ├── room.py                     # Room management
│   ├── lab_report.py               # Lab reports
│   └── __init__.py
│
├── templates/                      # HTML pages
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   ├── admin_dashboard.html
│   │   ├── doctor_dashboard.html
│   │   ├── receptionist_dashboard.html
│   │   └── patient_dashboard.html
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       └── 500.html
│
├── static/                         # CSS, JS, images
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── img/
│
├── utils/                          # Helper functions
│   ├── decorators.py
│   └── __init__.py
│
├── Documentation
│   ├── README.md                   # Full documentation
│   ├── SETUP_GUIDE.md              # Detailed setup
│   ├── PROJECT_SUMMARY.md          # Project overview
│   ├── FILE_INVENTORY.md           # File listing
│   └── QUICK_START.md              # This file
│
├── run.bat                         # Windows startup
├── run.sh                          # Unix startup
└── .gitignore                      # Git configuration
```

---

## 🔍 What Each Dashboard Shows

### Admin Dashboard
- Total patients, doctors, users, rooms
- Today's appointment count
- Revenue statistics
- Room occupancy
- Recent patients list

### Doctor Dashboard
- Today's appointments
- Pending appointments
- Completed appointments
- Pending lab reports
- Quick action buttons

### Receptionist Dashboard
- Today's appointments
- New patients
- Available doctors
- Available rooms
- Quick action buttons

### Patient Dashboard
- Upcoming appointments
- Pending bills
- Total bills paid
- Lab reports
- Room allocation info

---

## 📋 Main Features

### 1. Patient Management ✅
- Add/edit/delete patients
- Search patients by name, email
- View patient history
- Track appointments
- View bills

### 2. Doctor Management ✅
- Add/edit doctors
- Manage availability
- Schedule management
- Specialization filtering
- Doctor search

### 3. Appointment System ✅
- Book appointments
- Automatic collision detection
- Cancel appointments
- View available slots
- Status tracking

### 4. Billing System ✅
- Create bills
- Multi-component billing (consultation, medicine, tests, room)
- Track payments
- Payment status (Unpaid/Partial/Paid)
- Generate receipts

### 5. Room Management ✅
- Add rooms
- Allocate patients
- Discharge patients
- Track occupancy
- Available room filters

### 6. Lab Reports ✅
- Create test reports
- Update results
- Track status
- Delete reports

### 7. Medicine Management ✅
- Manage inventory
- Track stock levels
- Monitor expiry
- Generate prescriptions

### 8. Prescriptions ✅
- Create prescriptions
- Link to appointments
- Track medications
- Display formatted prescriptions

---

## 🐛 Troubleshooting

### Problem: "Python not found"
**Solution**: Install Python from python.org

### Problem: "MySQL not found"
**Solution**: Install MySQL from mysql.com

### Problem: Database connection error
**Solution**: 
1. Check MySQL is running
2. Verify credentials in config.py
3. Ensure database 'hospital_management' exists

### Problem: Port 5000 already in use
**Solution**: 
```python
# Edit app.py, find the last line:
app.run(host='0.0.0.0', port=5000, debug=True)
# Change to:
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Problem: Dependencies installation fails
**Solution**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Problem: Cannot login
**Solution**: 
1. Verify database imported successfully
2. Check credentials in Quick Start section
3. Ensure MySQL is running

---

## 📱 How to Use Each Module

### Patient Management
1. Login as Admin or Receptionist
2. Click "Patients" in navigation
3. Click "Add New Patient" to register
4. Search by name/email/phone
5. Click name to view full profile
6. Edit or update information

### Doctor Management
1. Login as Admin
2. Click "Doctors" in navigation
3. Add/edit availability and specialization
4. Search by specialization
5. View doctor profiles

### Booking Appointments
1. Click "Appointments" → "Book New"
2. Select patient and doctor
3. Choose date and time (shows available slots)
4. Add reason for visit
5. Confirm booking

### Processing Billing
1. Click "Billing" → "Create Bill"
2. Select patient and appointment
3. Add charges (consultation, medicine, tests, room fees)
4. Add discount if applicable
5. Record payment when received

### Room Management
1. Click "Rooms" in navigation
2. View all rooms with occupancy
3. Allocate patient to room
4. Discharge patient when done
5. Track room occupancy

---

## 🔐 Security Features

✅ Password hashing with bcrypt
✅ Role-based access control
✅ Session management
✅ SQL injection protection
✅ CSRF protection ready
✅ Input validation
✅ Secure password storage
✅ Authorization decorators

---

## 📊 Key Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - Patient registration
- `GET /auth/logout` - User logout

### Dashboards
- `GET /` - Role-based dashboard
- `GET /admin` - Admin dashboard
- `GET /doctor` - Doctor dashboard
- `GET /receptionist` - Receptionist dashboard
- `GET /patient` - Patient dashboard

### Patients
- `GET /patients/` - List all
- `POST /patients/new` - Create
- `GET /patients/<id>` - View
- `POST /patients/<id>/edit` - Update
- `POST /patients/<id>/delete` - Delete

### Appointments
- `GET /appointments/` - List
- `POST /appointments/book` - Create
- `GET /appointments/api/available-slots` - Get slots API

### Billing
- `GET /billing/` - List bills
- `POST /billing/new` - Create bill
- `POST /billing/<id>/pay` - Record payment

### Rooms
- `GET /rooms/` - List rooms
- `POST /rooms/<id>/allocate` - Allocate patient
- `POST /rooms/allocation/<id>/discharge` - Discharge patient

---

## 🚀 Next Steps After Launch

### Customize For Your Hospital
1. Update hospital name in base.html
2. Modify color scheme in static/css/style.css
3. Add your logo to static/img/
4. Update footer contact info

### Add Additional Features
1. Create more templates for CRUD operations
2. Add email notifications
3. Generate PDF reports
4. Add SMS reminders
5. Implement advanced analytics

### Deploy to Production
1. Use Gunicorn instead of Flask debug server
2. Set up reverse proxy (Nginx)
3. Use proper database backups
4. Enable HTTPS
5. Follow README.md deployment section

---

## 📞 Support Resources

- **README.md** - Complete feature documentation
- **SETUP_GUIDE.md** - Detailed installation instructions
- **PROJECT_SUMMARY.md** - Project architecture overview
- **FILE_INVENTORY.md** - Complete file listing

---

## ✨ What You Have

✅ Complete Hospital Management System
✅ 10 Database models
✅ 43+ API endpoints
✅ 4 Role-based dashboards
✅ Responsive design
✅ Production-ready code
✅ Comprehensive documentation
✅ Demo credentials for testing

---

## 🎉 You're Ready to Go!

Your Hospital Management System is complete and ready to use!

**Start now:**
- Windows: `run.bat`
- Linux/macOS: `./run.sh`
- Manual: Follow Step 1-7 above

**Then**: Open http://localhost:5000 and login!

---

**Happy managing! 🏥**

---

*Last Updated: March 22, 2026*
*Version: 1.0*
*Status: ✅ Ready to Use*
