"""
Room Allocation model for tracking patient admissions
"""
from datetime import datetime
from . import db

class RoomAllocation(db.Model):
    """Room Allocation model for managing patient room assignments"""
    __tablename__ = 'room_allocations'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), 
                          nullable=False, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id', ondelete='RESTRICT'), 
                       nullable=False, index=True)
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date)
    status = db.Column(db.Enum('Active', 'Discharged', 'Cancelled'), 
                      default='Active', index=True)
    reason_for_admission = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<RoomAllocation {self.patient_id} - {self.room_id}>'
    
    def is_active(self):
        """Check if allocation is active"""
        return self.status == 'Active' and self.discharge_date is None
    
    def get_length_of_stay(self):
        """Get length of stay in days"""
        from datetime import date
        end_date = self.discharge_date if self.discharge_date else date.today()
        delta = end_date - self.admission_date
        return delta.days
    
    def get_room_cost(self):
        """Calculate room cost based on length of stay"""
        if self.room and self.room.rate_per_day:
            length_of_stay = self.get_length_of_stay()
            return float(self.room.rate_per_day) * max(length_of_stay, 1)
        return 0
    
    def get_patient_info(self):
        """Get patient information"""
        if self.patient and self.patient.user:
            return {
                'id': self.patient.id,
                'name': self.patient.user.full_name,
                'email': self.patient.user.email,
                'phone': self.patient.user.phone
            }
        return None
    
    def get_room_info(self):
        """Get room information"""
        if self.room:
            return {
                'id': self.room.id,
                'room_number': self.room.room_number,
                'room_type': self.room.room_type,
                'rate_per_day': float(self.room.rate_per_day) if self.room.rate_per_day else 0
            }
        return None
    
    def to_dict(self):
        """Convert room allocation to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'room_id': self.room_id,
            'patient': self.get_patient_info(),
            'room': self.get_room_info(),
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
            'length_of_stay': self.get_length_of_stay(),
            'room_cost': self.get_room_cost(),
            'status': self.status,
            'reason_for_admission': self.reason_for_admission,
            'notes': self.notes
        }
