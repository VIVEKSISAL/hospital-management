"""
Lab Report management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, LabReport, Patient, Doctor
from utils.decorators import role_required
from datetime import datetime, date

lab_report_bp = Blueprint('lab_report', __name__, url_prefix='/lab-reports')

@lab_report_bp.route('/')
@login_required
def list_lab_reports():
    """List lab reports"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '', type=str)
    
    query = LabReport.query
    
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
    
    reports = query.order_by(LabReport.test_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('lab_report/list.html', reports=reports, status=status, user=current_user)

@lab_report_bp.route('/<int:report_id>')
@login_required
def view_report(report_id):
    """View lab report details"""
    report = LabReport.query.get_or_404(report_id)
    
    # Check authorization
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or report.patient_id != patient.id:
            return render_template('errors/404.html'), 404
    elif current_user.is_doctor():
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if doctor and report.doctor_id != doctor.id:
            if not current_user.is_admin():
                return render_template('errors/404.html'), 404
    
    return render_template('lab_report/view.html', report=report, user=current_user)

@lab_report_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Receptionist', 'Doctor')
def add_report():
    """Add new lab report"""
    if request.method == 'POST':
        patient_id = request.form.get('patient_id', type=int)
        test_name = request.form.get('test_name', '').strip()
        test_type = request.form.get('test_type', '')
        test_date = request.form.get('test_date', '')
        normal_range = request.form.get('normal_range', '')
        cost = request.form.get('cost', type=float)
        
        if not all([patient_id, test_name, test_date]):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('lab_report.add_report'))
        
        try:
            patient = Patient.query.get_or_404(patient_id)
            
            test_dt = datetime.strptime(test_date, '%Y-%m-%d').date()
            
            doctor_id = None
            if current_user.is_doctor():
                doctor = Doctor.query.filter_by(user_id=current_user.id).first()
                if doctor:
                    doctor_id = doctor.id
            elif request.form.get('doctor_id'):
                doctor_id = request.form.get('doctor_id', type=int)
            
            report = LabReport(
                patient_id=patient_id,
                doctor_id=doctor_id,
                test_name=test_name,
                test_type=test_type,
                test_date=test_dt,
                normal_range=normal_range,
                cost=cost,
                status='Pending'
            )
            db.session.add(report)
            db.session.commit()
            
            flash('Lab report created successfully', 'success')
            return redirect(url_for('lab_report.view_report', report_id=report.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating lab report: {str(e)}', 'danger')
            return redirect(url_for('lab_report.add_report'))
    
    return render_template('lab_report/add.html', user=current_user)

@lab_report_bp.route('/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Receptionist', 'Doctor')
def edit_report(report_id):
    """Edit lab report"""
    report = LabReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        try:
            report.test_name = request.form.get('test_name', report.test_name)
            report.test_type = request.form.get('test_type', report.test_type)
            report.result = request.form.get('result', report.result)
            report.status = request.form.get('status', report.status)
            report.normal_range = request.form.get('normal_range', report.normal_range)
            report.comments = request.form.get('comments', report.comments)
            report.cost = request.form.get('cost', type=float) or report.cost
            
            db.session.commit()
            flash('Lab report updated successfully', 'success')
            return redirect(url_for('lab_report.view_report', report_id=report.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating lab report: {str(e)}', 'danger')
    
    return render_template('lab_report/edit.html', report=report, user=current_user)

@lab_report_bp.route('/<int:report_id>/delete', methods=['POST'])
@login_required
@role_required('Admin', 'Receptionist')
def delete_report(report_id):
    """Delete lab report"""
    report = LabReport.query.get_or_404(report_id)
    
    try:
        patient_id = report.patient_id
        db.session.delete(report)
        db.session.commit()
        flash('Lab report deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting lab report: {str(e)}', 'danger')
    
    return redirect(url_for('patient.view_patient', patient_id=patient_id))
