"""
Appointment management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Appointment, Doctor, Patient
from utils.decorators import role_required
from datetime import datetime, date, timedelta

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointments')

@appointment_bp.route('/')
@login_required
def list_appointments():
    """List appointments"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '', type=str)
    
    query = Appointment.query
    
    # Filter by user role
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if patient:
            query = query.filter_by(patient_id=patient.id)
        else:
            return render_template('errors/404.html'), 404
    elif current_user.is_doctor():
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if doctor:
            query = query.filter_by(doctor_id=doctor.id)
        else:
            return render_template('errors/404.html'), 404
    elif not (current_user.is_admin() or current_user.is_receptionist()):
        return render_template('errors/404.html'), 404
    
    if status:
        query = query.filter_by(status=status)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('appointment/list.html', appointments=appointments, status=status, user=current_user)

@appointment_bp.route('/<int:appointment_id>')
@login_required
def view_appointment(appointment_id):
    """View appointment details"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check authorization
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or appointment.patient_id != patient.id:
            return render_template('errors/404.html'), 404
    elif current_user.is_doctor():
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor or appointment.doctor_id != doctor.id:
            return render_template('errors/404.html'), 404
    
    return render_template('appointment/view.html', appointment=appointment, user=current_user)

@appointment_bp.route('/book', methods=['GET', 'POST'])
@login_required
@role_required('Receptionist', 'Patient')
def book_appointment():
    """Book new appointment"""
    patient = None
    
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        if current_user.is_receptionist():
            patient_id = request.form.get('patient_id', type=int)
            patient = Patient.query.get_or_404(patient_id)
        
        doctor_id = request.form.get('doctor_id', type=int)
        appointment_date = request.form.get('appointment_date', '')
        appointment_time = request.form.get('appointment_time', '')
        reason_for_visit = request.form.get('reason_for_visit', '')
        
        if not all([patient, doctor_id, appointment_date, appointment_time]):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('appointment.book_appointment'))
        
        try:
            doctor = Doctor.query.get_or_404(doctor_id)
            apt_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            apt_time = datetime.strptime(appointment_time, '%H:%M').time()
            
            # Validate date is not in the past
            if apt_date < date.today():
                flash('Appointment date cannot be in the past', 'danger')
                return redirect(url_for('appointment.book_appointment'))
            
            # Check for double booking
            existing = Appointment.query.filter(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == apt_date,
                Appointment.appointment_time == apt_time,
                Appointment.status != 'Cancelled'
            ).first()
            
            if existing:
                flash('This time slot is already booked. Please choose another time.', 'danger')
                return redirect(url_for('appointment.book_appointment'))
            
            # Create appointment
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=doctor_id,
                appointment_date=apt_date,
                appointment_time=apt_time,
                reason_for_visit=reason_for_visit
            )
            db.session.add(appointment)
            db.session.commit()
            
            flash('Appointment booked successfully', 'success')
            return redirect(url_for('appointment.view_appointment', appointment_id=appointment.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error booking appointment: {str(e)}', 'danger')
            return redirect(url_for('appointment.book_appointment'))
    
    return render_template('appointment/book.html', patient=patient, user=current_user)

@appointment_bp.route('/<int:appointment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    """Edit appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check authorization
    if not current_user.is_admin() and not current_user.is_receptionist():
        return render_template('errors/404.html'), 404
    
    if request.method == 'POST':
        try:
            appointment.appointment_date = datetime.strptime(
                request.form.get('appointment_date', ''), '%Y-%m-%d'
            ).date()
            
            appointment.appointment_time = datetime.strptime(
                request.form.get('appointment_time', ''), '%H:%M'
            ).time()
            
            appointment.status = request.form.get('status', appointment.status)
            appointment.reason_for_visit = request.form.get('reason_for_visit', appointment.reason_for_visit)
            appointment.notes = request.form.get('notes', appointment.notes)
            
            db.session.commit()
            flash('Appointment updated successfully', 'success')
            return redirect(url_for('appointment.view_appointment', appointment_id=appointment.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating appointment: {str(e)}', 'danger')
    
    return render_template('appointment/edit.html', appointment=appointment, user=current_user)

@appointment_bp.route('/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    """Cancel appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check authorization
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or appointment.patient_id != patient.id:
            return redirect(url_for('dashboard.index'))
    elif not (current_user.is_admin() or current_user.is_receptionist()):
        return redirect(url_for('dashboard.index'))
    
    if appointment.can_be_cancelled():
        try:
            appointment.status = 'Cancelled'
            db.session.commit()
            flash('Appointment cancelled successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error cancelling appointment: {str(e)}', 'danger')
    else:
        flash('This appointment cannot be cancelled', 'danger')
    
    return redirect(url_for('appointment.view_appointment', appointment_id=appointment.id))

@appointment_bp.route('/api/available-slots')
@login_required
def get_available_slots():
    """Get available appointment slots for a doctor"""
    doctor_id = request.args.get('doctor_id', type=int)
    appointment_date = request.args.get('date', '')
    
    if not doctor_id or not appointment_date:
        return jsonify([])
    
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor or not doctor.available_from or not doctor.available_to:
            return jsonify([])
        
        apt_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        
        # Generate time slots
        current_time = datetime.combine(apt_date, doctor.available_from)
        end_time = datetime.combine(apt_date, doctor.available_to)
        slots = []
        
        while current_time < end_time:
            slot_time = current_time.time()
            
            # Check if slot is already booked
            booked = Appointment.query.filter(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == apt_date,
                Appointment.appointment_time == slot_time,
                Appointment.status != 'Cancelled'
            ).first()
            
            if not booked:
                slots.append(slot_time.isoformat(timespec='minutes'))
            
            current_time += timedelta(minutes=doctor.consultation_duration or 30)
        
        return jsonify(slots)
    
    except Exception as e:
        return jsonify([])
