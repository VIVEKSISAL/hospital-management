"""
Billing management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Billing, Patient, Appointment
from utils.decorators import role_required
from datetime import datetime, date

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

@billing_bp.route('/')
@login_required
def list_bills():
    """List billings"""
    page = request.args.get('page', 1, type=int)
    payment_status = request.args.get('payment_status', '', type=str)
    
    query = Billing.query
    
    # Filter by user role
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if patient:
            query = query.filter_by(patient_id=patient.id)
        else:
            return render_template('errors/404.html'), 404
    elif not (current_user.is_admin() or current_user.is_receptionist()):
        return render_template('errors/404.html'), 404
    
    if payment_status:
        query = query.filter_by(payment_status=payment_status)
    
    bills = query.order_by(Billing.billing_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('billing/list.html', bills=bills, payment_status=payment_status, user=current_user)

@billing_bp.route('/<int:bill_id>')
@login_required
def view_bill(bill_id):
    """View bill details"""
    bill = Billing.query.get_or_404(bill_id)
    
    # Check authorization
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or bill.patient_id != patient.id:
            return render_template('errors/404.html'), 404
    
    return render_template('billing/view.html', bill=bill, user=current_user)

@billing_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Receptionist')
def add_bill():
    """Create new billing"""
    if request.method == 'POST':
        patient_id = request.form.get('patient_id', type=int)
        appointment_id = request.form.get('appointment_id', type=int)
        consultation_fee = request.form.get('consultation_fee', type=float)
        medicine_cost = request.form.get('medicine_cost', type=float)
        test_cost = request.form.get('test_cost', type=float)
        room_cost = request.form.get('room_cost', type=float)
        other_charges = request.form.get('other_charges', type=float)
        discount = request.form.get('discount', type=float)
        notes = request.form.get('notes', '')
        
        if not patient_id:
            flash('Please select a patient', 'danger')
            return redirect(url_for('billing.add_bill'))
        
        try:
            patient = Patient.query.get_or_404(patient_id)
            
            bill = Billing(
                patient_id=patient_id,
                appointment_id=appointment_id,
                billing_date=date.today(),
                consultation_fee=consultation_fee or 0,
                medicine_cost=medicine_cost or 0,
                test_cost=test_cost or 0,
                room_cost=room_cost or 0,
                other_charges=other_charges or 0,
                discount=discount or 0,
                notes=notes
            )
            
            bill.calculate_payment_status()
            db.session.add(bill)
            db.session.commit()
            
            flash('Bill created successfully', 'success')
            return redirect(url_for('billing.view_bill', bill_id=bill.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating bill: {str(e)}', 'danger')
            return redirect(url_for('billing.add_bill'))
    
    return render_template('billing/add.html', user=current_user)

@billing_bp.route('/<int:bill_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Receptionist')
def edit_bill(bill_id):
    """Edit billing"""
    bill = Billing.query.get_or_404(bill_id)
    
    if request.method == 'POST':
        try:
            bill.consultation_fee = request.form.get('consultation_fee', type=float) or bill.consultation_fee
            bill.medicine_cost = request.form.get('medicine_cost', type=float) or bill.medicine_cost
            bill.test_cost = request.form.get('test_cost', type=float) or bill.test_cost
            bill.room_cost = request.form.get('room_cost', type=float) or bill.room_cost
            bill.other_charges = request.form.get('other_charges', type=float) or bill.other_charges
            bill.discount = request.form.get('discount', type=float) or bill.discount
            bill.notes = request.form.get('notes', bill.notes)
            
            bill.calculate_payment_status()
            db.session.commit()
            flash('Bill updated successfully', 'success')
            return redirect(url_for('billing.view_bill', bill_id=bill.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating bill: {str(e)}', 'danger')
    
    return render_template('billing/edit.html', bill=bill, user=current_user)

@billing_bp.route('/<int:bill_id>/pay', methods=['GET', 'POST'])
@login_required
def pay_bill(bill_id):
    """Record payment for bill"""
    bill = Billing.query.get_or_404(bill_id)
    
    # Check authorization
    if current_user.is_patient():
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or bill.patient_id != patient.id:
            return render_template('errors/404.html'), 404
    elif not (current_user.is_admin() or current_user.is_receptionist()):
        return render_template('errors/404.html'), 404
    
    if request.method == 'POST':
        amount_paid = request.form.get('amount_paid', type=float)
        payment_method = request.form.get('payment_method', '')
        
        if not amount_paid or amount_paid <= 0:
            flash('Please enter valid payment amount', 'danger')
            return redirect(url_for('billing.pay_bill', bill_id=bill.id))
        
        try:
            bill.amount_paid = (bill.amount_paid or 0) + amount_paid
            bill.payment_method = payment_method
            bill.calculate_payment_status()
            db.session.commit()
            
            flash(f'Payment of ${amount_paid} recorded successfully', 'success')
            return redirect(url_for('billing.view_bill', bill_id=bill.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording payment: {str(e)}', 'danger')
    
    return render_template('billing/pay.html', bill=bill, user=current_user)

@billing_bp.route('/api/patient-bills')
@login_required
@role_required('Admin', 'Receptionist')
def get_patient_bills():
    """Get bills for a patient"""
    patient_id = request.args.get('patient_id', type=int)
    
    if not patient_id:
        return jsonify([])
    
    bills = Billing.query.filter_by(patient_id=patient_id).all()
    
    return jsonify([{
        'id': bill.id,
        'date': bill.billing_date.isoformat(),
        'total': bill.get_total_amount(),
        'due': bill.get_amount_due(),
        'status': bill.payment_status
    } for bill in bills])
