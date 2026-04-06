"""
Dashboard routes for different user roles
"""
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import db, User, Patient, Doctor, Appointment, Billing, LabReport, Room, RoomAllocation, Medicine
from datetime import datetime, timedelta, date
from utils.decorators import role_required
from sqlalchemy import func, and_

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard - route to role-specific dashboard"""
    if current_user.is_admin():
        return redirect(url_for('dashboard.admin_dashboard'))
    elif current_user.is_doctor():
        return redirect(url_for('dashboard.doctor_dashboard'))
    elif current_user.is_receptionist():
        return redirect(url_for('dashboard.receptionist_dashboard'))
    elif current_user.is_patient():
        return redirect(url_for('dashboard.patient_dashboard'))
    else:
        return redirect(url_for('auth.login'))

@dashboard_bp.route('/admin')
@login_required
@role_required('Admin')
def admin_dashboard():
    """Admin dashboard with statistics"""
    today = date.today()
    month_ago = today - timedelta(days=30)
    
    # Statistics
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_users = User.query.count()
    total_rooms = Room.query.count()
    
    # Today's appointments
    todays_appointments = Appointment.query.filter(
        Appointment.appointment_date == today,
        Appointment.status == 'Scheduled'
    ).count()
    
    # Recent billings
    total_revenue = db.session.query(func.sum(Billing.amount_paid)).filter(
        Billing.billing_date >= month_ago
    ).scalar() or 0
    
    # Upcoming appointments this week
    week_later = today + timedelta(days=7)
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date <= week_later,
        Appointment.appointment_date >= today,
        Appointment.status == 'Scheduled'
    ).count()
    
    # Room occupancy
    occupied_rooms = Room.query.filter(Room.occupied_beds > 0).count()
    
    # Recent patients
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    
    # Pending bills
    pending_bills = Billing.query.filter(
        Billing.payment_status != 'Paid'
    ).count()
    
    stats = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_users': total_users,
        'total_rooms': total_rooms,
        'todays_appointments': todays_appointments,
        'total_revenue': float(total_revenue),
        'upcoming_appointments': upcoming_appointments,
        'occupied_rooms': occupied_rooms,
        'pending_bills': pending_bills
    }
    
    return render_template('dashboard/admin_dashboard.html', 
                         stats=stats, 
                         recent_patients=recent_patients,
                         user=current_user)

@dashboard_bp.route('/doctor')
@login_required
@role_required('Doctor')
def doctor_dashboard():
    """Doctor dashboard"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    today = date.today()
    
    if not doctor:
        return render_template('errors/404.html'), 404
    
    # Get today's appointments
    todays_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date == today,
        Appointment.status == 'Scheduled'
    ).all()
    
    # Get pending appointments
    pending_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == 'Scheduled',
        Appointment.appointment_date >= today
    ).count()
    
    # Get completed appointments this month
    month_ago = today - timedelta(days=30)
    completed_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == 'Completed',
        Appointment.appointment_date >= month_ago
    ).count()
    
    # Get pending lab reports
    pending_reports = db.session.query(LabReport).filter(
        LabReport.doctor_id == doctor.id,
        LabReport.status == 'Pending'
    ).count()
    
    stats = {
        'todays_appointments': len(todays_appointments),
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'pending_reports': pending_reports
    }
    
    return render_template('dashboard/doctor_dashboard.html',
                         doctor=doctor,
                         todays_appointments=todays_appointments,
                         stats=stats,
                         user=current_user)

@dashboard_bp.route('/receptionist')
@login_required
@role_required('Receptionist')
def receptionist_dashboard():
    """Receptionist dashboard"""
    today = date.today()
    
    # Today's appointments
    todays_appointments = Appointment.query.filter(
        Appointment.appointment_date == today
    ).count()
    
    # Pending appointments
    pending_appointments = Appointment.query.filter(
        Appointment.status == 'Scheduled',
        Appointment.appointment_date >= today
    ).count()
    
    # New patients registered today
    new_patients = Patient.query.filter(
        Patient.created_at >= datetime.combine(today, datetime.min.time()),
        Patient.created_at <= datetime.combine(today, datetime.max.time())
    ).count()
    
    # Available doctors
    available_doctors = Doctor.query.filter_by(is_available=True).count()
    
    # Available rooms
    available_rooms = Room.query.filter(
        Room.is_available == True,
        Room.occupied_beds < Room.capacity
    ).count()
    
    stats = {
        'todays_appointments': todays_appointments,
        'pending_appointments': pending_appointments,
        'new_patients': new_patients,
        'available_doctors': available_doctors,
        'available_rooms': available_rooms
    }
    
    return render_template('dashboard/receptionist_dashboard.html',
                         stats=stats,
                         user=current_user)

@dashboard_bp.route('/patient')
@login_required
@role_required('Patient')
def patient_dashboard():
    """Patient dashboard"""
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if not patient:
        return render_template('errors/404.html'), 404
    
    today = date.today()
    
    # Upcoming appointments
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= today,
        Appointment.status == 'Scheduled'
    ).all()
    
    # Recent bills
    recent_bills = Billing.query.filter_by(patient_id=patient.id).order_by(
        Billing.billing_date.desc()
    ).limit(5).all()
    
    # Pending bills
    pending_bills = Billing.query.filter(
        Billing.patient_id == patient.id,
        Billing.payment_status != 'Paid'
    ).all()
    
    # Lab reports
    lab_reports = LabReport.query.filter_by(patient_id=patient.id).order_by(
        LabReport.test_date.desc()
    ).limit(5).all()
    
    # Room allocation info
    current_room_allocation = RoomAllocation.query.filter(
        RoomAllocation.patient_id == patient.id,
        RoomAllocation.status == 'Active'
    ).first()
    
    stats = {
        'upcoming_appointments': len(upcoming_appointments),
        'pending_bills': len(pending_bills),
        'total_bills': Billing.query.filter_by(patient_id=patient.id).count(),
        'lab_reports': len(lab_reports)
    }
    
    return render_template('dashboard/patient_dashboard.html',
                         patient=patient,
                         upcoming_appointments=upcoming_appointments,
                         recent_bills=recent_bills,
                         pending_bills=pending_bills,
                         lab_reports=lab_reports,
                         current_room_allocation=current_room_allocation,
                         stats=stats,
                         user=current_user)

@dashboard_bp.route('/api/chart-data')
@login_required
@role_required('Admin')
def chart_data():
    """Get chart data for dashboard"""
    today = date.today()
    
    # Patients by gender
    patients_by_gender = db.session.query(
        Patient.gender,
        func.count(Patient.id).label('count')
    ).group_by(Patient.gender).all()
    
    # Appointments this month
    month_ago = today - timedelta(days=30)
    appointments_this_month = db.session.query(
        Appointment.appointment_date,
        func.count(Appointment.id).label('count')
    ).filter(
        Appointment.appointment_date >= month_ago,
        Appointment.appointment_date <= today
    ).group_by(Appointment.appointment_date).all()
    
    # Room occupancy
    room_occupancy = db.session.query(
        Room.room_type,
        func.avg(Room.occupied_beds).label('avg_occupied')
    ).group_by(Room.room_type).all()
    
    data = {
        'patients_by_gender': {item[0]: item[1] for item in patients_by_gender},
        'appointments_this_month': {str(item[0]): item[1] for item in appointments_this_month},
        'room_occupancy': {item[0]: float(item[1]) if item[1] else 0 for item in room_occupancy}
    }
    
    return jsonify(data)
