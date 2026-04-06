"""
Doctor management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Doctor
from utils.decorators import role_required
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctors')

@doctor_bp.route('/')
@login_required
@role_required('Admin', 'Receptionist')
def list_doctors():
    """List all doctors"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    specialization = request.args.get('specialization', '', type=str)
    
    query = Doctor.query.join(User).filter(User.is_active == True)
    
    if search:
        query = query.filter(
            (User.full_name.ilike(f'%{search}%')) |
            (Doctor.specialization.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
    
    doctors = query.order_by(Doctor.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('doctor/list.html', doctors=doctors, search=search, 
                         specialization=specialization, user=current_user)

@doctor_bp.route('/<int:doctor_id>')
@login_required
def view_doctor(doctor_id):
    """View doctor details"""
    doctor = Doctor.query.get_or_404(doctor_id)
    
    return render_template('doctor/view.html', doctor=doctor, user=current_user)

@doctor_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def add_doctor():
    """Add new doctor"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        specialization = request.form.get('specialization', '').strip()
        license_number = request.form.get('license_number', '').strip()
        experience_years = request.form.get('experience_years', type=int)
        qualification = request.form.get('qualification', '')
        clinic_address = request.form.get('clinic_address', '')
        consultation_fee = request.form.get('consultation_fee', type=float)
        available_from = request.form.get('available_from', '')
        available_to = request.form.get('available_to', '')
        
        # Validation
        if not all([username, email, password, full_name, specialization]):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('doctor.add_doctor'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('doctor.add_doctor'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('doctor.add_doctor'))
        
        if license_number and Doctor.query.filter_by(license_number=license_number).first():
            flash('License number already exists', 'danger')
            return redirect(url_for('doctor.add_doctor'))
        
        try:
            # Create user
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                role='Doctor'
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()
            
            # Parse times
            available_from_time = datetime.strptime(available_from, '%H:%M').time() if available_from else None
            available_to_time = datetime.strptime(available_to, '%H:%M').time() if available_to else None
            
            # Create doctor record
            doctor = Doctor(
                user_id=new_user.id,
                specialization=specialization,
                license_number=license_number,
                experience_years=experience_years,
                qualification=qualification,
                clinic_address=clinic_address,
                consultation_fee=consultation_fee,
                available_from=available_from_time,
                available_to=available_to_time
            )
            db.session.add(doctor)
            db.session.commit()
            
            flash(f'Doctor {full_name} added successfully', 'success')
            return redirect(url_for('doctor.view_doctor', doctor_id=doctor.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding doctor: {str(e)}', 'danger')
            return redirect(url_for('doctor.add_doctor'))
    
    return render_template('doctor/add.html', user=current_user)

@doctor_bp.route('/<int:doctor_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def edit_doctor(doctor_id):
    """Edit doctor details"""
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if request.method == 'POST':
        try:
            doctor.specialization = request.form.get('specialization', doctor.specialization)
            doctor.experience_years = request.form.get('experience_years', type=int) or doctor.experience_years
            doctor.qualification = request.form.get('qualification', doctor.qualification)
            doctor.clinic_address = request.form.get('clinic_address', doctor.clinic_address)
            doctor.consultation_fee = request.form.get('consultation_fee', type=float) or doctor.consultation_fee
            
            available_from = request.form.get('available_from', '')
            available_to = request.form.get('available_to', '')
            
            if available_from:
                doctor.available_from = datetime.strptime(available_from, '%H:%M').time()
            if available_to:
                doctor.available_to = datetime.strptime(available_to, '%H:%M').time()
            
            if current_user.is_admin():
                doctor.user.phone = request.form.get('phone', doctor.user.phone)
                doctor.is_available = request.form.get('is_available') == 'on'
            
            db.session.commit()
            flash('Doctor updated successfully', 'success')
            return redirect(url_for('doctor.view_doctor', doctor_id=doctor.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating doctor: {str(e)}', 'danger')
    
    return render_template('doctor/edit.html', doctor=doctor, user=current_user)

@doctor_bp.route('/<int:doctor_id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_doctor(doctor_id):
    """Delete doctor record"""
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor_name = doctor.user.full_name if doctor.user else 'Unknown'
    user_id = doctor.user_id
    
    try:
        db.session.delete(doctor)
        if user_id:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
        db.session.commit()
        flash(f'Doctor {doctor_name} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting doctor: {str(e)}', 'danger')
    
    return redirect(url_for('doctor.list_doctors'))

@doctor_bp.route('/api/specializations')
@login_required
def get_specializations():
    """Get list of specializations"""
    specializations = db.session.query(Doctor.specialization).distinct().all()
    return jsonify([s[0] for s in specializations if s[0]])

@doctor_bp.route('/api/search')
@login_required
@role_required('Admin', 'Receptionist', 'Patient')
def search_doctors():
    """Search doctors API"""
    search = request.args.get('q', '', type=str)
    specialization = request.args.get('specialization', '', type=str)
    
    query = Doctor.query.join(User).filter(
        User.is_active == True,
        Doctor.is_available == True
    )
    
    if search:
        query = query.filter(
            (User.full_name.ilike(f'%{search}%')) |
            (Doctor.specialization.ilike(f'%{search}%'))
        )
    
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
    
    doctors = query.limit(10).all()
    
    results = []
    for doctor in doctors:
        if doctor.user:
            results.append({
                'id': doctor.id,
                'name': doctor.user.full_name,
                'specialization': doctor.specialization,
                'email': doctor.user.email,
                'phone': doctor.user.phone,
                'consultation_fee': float(doctor.consultation_fee) if doctor.consultation_fee else 0
            })
    
    return jsonify(results)
