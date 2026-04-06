"""
Room/Ward management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Room, RoomAllocation, Patient
from utils.decorators import role_required
from datetime import datetime, date

room_bp = Blueprint('room', __name__, url_prefix='/rooms')

@room_bp.route('/')
@login_required
@role_required('Admin', 'Receptionist')
def list_rooms():
    """List all rooms"""
    page = request.args.get('page', 1, type=int)
    room_type = request.args.get('room_type', '', type=str)
    available_only = request.args.get('available_only', 'false') == 'true'
    
    query = Room.query
    
    if room_type:
        query = query.filter_by(room_type=room_type)
    
    if available_only:
        query = query.filter(Room.is_available == True)
    
    rooms = query.order_by(Room.room_number).paginate(page=page, per_page=10)
    
    return render_template('room/list.html', rooms=rooms, room_type=room_type, 
                         available_only=available_only, user=current_user)

@room_bp.route('/<int:room_id>')
@login_required
@role_required('Admin', 'Receptionist')
def view_room(room_id):
    """View room details"""
    room = Room.query.get_or_404(room_id)
    allocations = room.room_allocations
    
    return render_template('room/view.html', room=room, allocations=allocations, user=current_user)

@room_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def add_room():
    """Add new room"""
    if request.method == 'POST':
        room_number = request.form.get('room_number', '').strip()
        room_type = request.form.get('room_type', '')
        floor = request.form.get('floor', type=int)
        capacity = request.form.get('capacity', type=int)
        rate_per_day = request.form.get('rate_per_day', type=float)
        facilities = request.form.get('facilities', '')
        
        if not all([room_number, room_type, capacity]):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('room.add_room'))
        
        if Room.query.filter_by(room_number=room_number).first():
            flash('Room number already exists', 'danger')
            return redirect(url_for('room.add_room'))
        
        try:
            room = Room(
                room_number=room_number,
                room_type=room_type,
                floor=floor,
                capacity=capacity,
                rate_per_day=rate_per_day,
                facilities=facilities
            )
            db.session.add(room)
            db.session.commit()
            
            flash(f'Room {room_number} added successfully', 'success')
            return redirect(url_for('room.view_room', room_id=room.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding room: {str(e)}', 'danger')
            return redirect(url_for('room.add_room'))
    
    return render_template('room/add.html', user=current_user)

@room_bp.route('/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def edit_room(room_id):
    """Edit room"""
    room = Room.query.get_or_404(room_id)
    
    if request.method == 'POST':
        try:
            room.room_type = request.form.get('room_type', room.room_type)
            room.floor = request.form.get('floor', type=int) or room.floor
            room.capacity = request.form.get('capacity', type=int) or room.capacity
            room.rate_per_day = request.form.get('rate_per_day', type=float) or room.rate_per_day
            room.facilities = request.form.get('facilities', room.facilities)
            room.is_available = request.form.get('is_available') == 'on'
            
            db.session.commit()
            flash('Room updated successfully', 'success')
            return redirect(url_for('room.view_room', room_id=room.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating room: {str(e)}', 'danger')
    
    return render_template('room/edit.html', room=room, user=current_user)

@room_bp.route('/<int:room_id>/allocate', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Receptionist')
def allocate_room(room_id):
    """Allocate room to patient"""
    room = Room.query.get_or_404(room_id)
    
    if request.method == 'POST':
        patient_id = request.form.get('patient_id', type=int)
        admission_date = request.form.get('admission_date', '')
        reason_for_admission = request.form.get('reason_for_admission', '')
        notes = request.form.get('notes', '')
        
        if not all([patient_id, admission_date]):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('room.allocate_room', room_id=room_id))
        
        try:
            patient = Patient.query.get_or_404(patient_id)
            admission_dt = datetime.strptime(admission_date, '%Y-%m-%d').date()
            
            # Check if patient is already admitted
            active_allocation = RoomAllocation.query.filter(
                RoomAllocation.patient_id == patient_id,
                RoomAllocation.status == 'Active'
            ).first()
            
            if active_allocation:
                flash('Patient is already admitted to a room', 'danger')
                return redirect(url_for('room.allocate_room', room_id=room_id))
            
            # Allocate room
            allocation = RoomAllocation(
                patient_id=patient_id,
                room_id=room_id,
                admission_date=admission_dt,
                reason_for_admission=reason_for_admission,
                notes=notes
            )
            
            room.occupied_beds += 1
            
            db.session.add(allocation)
            db.session.commit()
            
            flash(f'Patient allocated to room {room.room_number} successfully', 'success')
            return redirect(url_for('room.view_room', room_id=room_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error allocating room: {str(e)}', 'danger')
            return redirect(url_for('room.allocate_room', room_id=room_id))
    
    return render_template('room/allocate.html', room=room, user=current_user)

@room_bp.route('/allocation/<int:allocation_id>/discharge', methods=['POST'])
@login_required
@role_required('Admin', 'Receptionist')
def discharge_patient(allocation_id):
    """Discharge patient from room"""
    allocation = RoomAllocation.query.get_or_404(allocation_id)
    
    try:
        allocation.status = 'Discharged'
        allocation.discharge_date = date.today()
        
        room = allocation.room
        room.occupied_beds = max(0, room.occupied_beds - 1)
        
        db.session.commit()
        flash('Patient discharged successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error discharging patient: {str(e)}', 'danger')
    
    return redirect(url_for('room.view_room', room_id=allocation.room_id))

@room_bp.route('/api/available-rooms')
@login_required
@role_required('Admin', 'Receptionist', 'Patient')
def get_available_rooms():
    """Get available rooms"""
    room_type = request.args.get('room_type', '', type=str)
    
    query = Room.query.filter(
        Room.is_available == True,
        Room.occupied_beds < Room.capacity
    )
    
    if room_type:
        query = query.filter_by(room_type=room_type)
    
    rooms = query.all()
    
    return jsonify([{
        'id': room.id,
        'room_number': room.room_number,
        'room_type': room.room_type,
        'available_beds': room.get_available_beds(),
        'rate_per_day': float(room.rate_per_day) if room.rate_per_day else 0
    } for room in rooms])
