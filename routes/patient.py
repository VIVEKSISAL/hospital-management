"""
Patient management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Patient
from utils.decorators import role_required
from datetime import datetime

patient_bp = Blueprint('patient', __name__, url_prefix='/patients')

@patient_bp.route('/')
@login_required
@role_required('Admin', 'Receptionist')
def list_patients():
    """List all patients"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Patient.query.join(User).filter(User.is_active == True)
    
    if search:
        query = query.filter(
            (User.full_name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.phone.ilike(f'%{search}%'))
        )
    
    patients = query.order_by(Patient.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('patient/list.html', patients=patients, search=search, user=current_user)

@patient_bp.route('/<int:patient_id>')
@login_required
def view_patient(patient_id):
    """View patient details"""
    patient = Patient.query.get_or_404(patient_id)
    
    # Check authorization
    if not current_user.is_admin() and not current_user.is_receptionist():
        if not (current_user.is_patient() and patient.user_id == current_user.id):
            return render_template('errors/404.html'), 404
    
    return render_template('patient/view.html', patient=patient, user=current_user)

@patient_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Receptionist')
def add_patient():
    """Add new patient"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        date_of_birth = request.form.get('date_of_birth', '')
        gender = request.form.get('gender', '')
        blood_group = request.form.get('blood_group', '')
        address = request.form.get('address', '')
        city = request.form.get('city', '')
        state = request.form.get('state', '')
        zip_code = request.form.get('zip_code', '')
        emergency_contact = request.form.get('emergency_contact', '')
        emergency_contact_name = request.form.get('emergency_contact_name', '')
        medical_history = request.form.get('medical_history', '')
        allergies = request.form.get('allergies', '')
        current_medications = request.form.get('current_medications', '')
        
        # Validation
        if not all([username, email, password, full_name, gender]):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('patient.add_patient'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('patient.add_patient'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('patient.add_patient'))
        
        try:
            # Create user
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                role='Patient'
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()
            
            # Create patient record
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None
            
            patient = Patient(
                user_id=new_user.id,
                date_of_birth=dob,
                gender=gender,
                blood_group=blood_group,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                emergency_contact=emergency_contact,
                emergency_contact_name=emergency_contact_name,
                medical_history=medical_history,
                allergies=allergies,
                current_medications=current_medications
            )
            db.session.add(patient)
            db.session.commit()
            
            flash(f'Patient {full_name} added successfully', 'success')
            return redirect(url_for('patient.view_patient', patient_id=patient.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding patient: {str(e)}', 'danger')
            return redirect(url_for('patient.add_patient'))
    
    return render_template('patient/add.html', user=current_user)

@patient_bp.route('/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    """Edit patient details"""
    patient = Patient.query.get_or_404(patient_id)
    
    # Check authorization
    if not current_user.is_admin() and not current_user.is_receptionist():
        if not (current_user.is_patient() and patient.user_id == current_user.id):
            return render_template('errors/404.html'), 404
    
    if request.method == 'POST':
        try:
            patient.date_of_birth = datetime.strptime(
                request.form.get('date_of_birth', ''), '%Y-%m-%d'
            ).date() if request.form.get('date_of_birth') else patient.date_of_birth
            
            patient.gender = request.form.get('gender', patient.gender)
            patient.blood_group = request.form.get('blood_group', patient.blood_group)
            patient.address = request.form.get('address', patient.address)
            patient.city = request.form.get('city', patient.city)
            patient.state = request.form.get('state', patient.state)
            patient.zip_code = request.form.get('zip_code', patient.zip_code)
            patient.emergency_contact = request.form.get('emergency_contact', patient.emergency_contact)
            patient.emergency_contact_name = request.form.get('emergency_contact_name', patient.emergency_contact_name)
            patient.medical_history = request.form.get('medical_history', patient.medical_history)
            patient.allergies = request.form.get('allergies', patient.allergies)
            patient.current_medications = request.form.get('current_medications', patient.current_medications)
            
            # Update user info if changed
            if current_user.is_admin() or current_user.is_receptionist():
                patient.user.phone = request.form.get('phone', patient.user.phone)
            
            db.session.commit()
            flash('Patient updated successfully', 'success')
            return redirect(url_for('patient.view_patient', patient_id=patient.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating patient: {str(e)}', 'danger')
    
    return render_template('patient/edit.html', patient=patient, user=current_user)

@patient_bp.route('/<int:patient_id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_patient(patient_id):
    """Delete patient record"""
    patient = Patient.query.get_or_404(patient_id)
    patient_name = patient.user.full_name if patient.user else 'Unknown'
    user_id = patient.user_id
    
    try:
        db.session.delete(patient)
        if user_id:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
        db.session.commit()
        flash(f'Patient {patient_name} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting patient: {str(e)}', 'danger')
    
    return redirect(url_for('patient.list_patients'))

@patient_bp.route('/api/search')
@login_required
@role_required('Admin', 'Receptionist', 'Doctor')
def search_patients():
    """Search patients API"""
    search = request.args.get('q', '', type=str)
    
    if len(search) < 2:
        return jsonify([])
    
    patients = Patient.query.join(User).filter(
        (User.full_name.ilike(f'%{search}%')) |
        (User.email.ilike(f'%{search}%')) |
        (User.phone.ilike(f'%{search}%'))
    ).limit(10).all()
    
    results = []
    for patient in patients:
        if patient.user:
            results.append({
                'id': patient.id,
                'name': patient.user.full_name,
                'email': patient.user.email,
                'phone': patient.user.phone,
                'age': patient.get_age()
            })
    
    return jsonify(results)
