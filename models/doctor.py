"""
Doctor model for doctor management
"""
from datetime import datetime
from . import db

class Doctor(db.Model):
    """Doctor model for storing doctor information"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), 
                       unique=True, nullable=True)
    specialization = db.Column(db.String(100), nullable=False, index=True)
    license_number = db.Column(db.String(50), unique=True)
    experience_years = db.Column(db.Integer)
    qualification = db.Column(db.String(200))
    clinic_address = db.Column(db.String(255))
    consultation_fee = db.Column(db.DECIMAL(10, 2))
    available_from = db.Column(db.Time)
    available_to = db.Column(db.Time)
    consultation_duration = db.Column(db.Integer, default=30)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', cascade='all, delete-orphan')
    lab_reports = db.relationship('LabReport', backref='doctor', cascade='all, delete-orphan')
    prescriptions = db.relationship('Prescription', backref='doctor', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Doctor {self.user.full_name if self.user else "Unknown"}>'
    
    def get_scheduled_appointments(self, date=None):
        """Get scheduled appointments for a doctor"""
        from datetime import date as dateobj
        if date is None:
            date = dateobj.today()
        
        return [apt for apt in self.appointments 
                if apt.appointment_date == date and apt.status == 'Scheduled']
    
    def get_available_slots(self, date=None):
        """Get available appointment slots for the day"""
        # This would need more complex logic based on available_from, available_to
        # and consultation_duration
        scheduled = self.get_scheduled_appointments(date)
        return len(scheduled) < 10  # Simple check, implement as needed
    
    def get_today_appointments(self):
        """Get today's appointments"""
        from datetime import date
        return self.get_scheduled_appointments(date.today())
    
    def get_appointment_count(self):
        """Get total appointment count"""
        return len(self.appointments)
    
    def to_dict(self):
        """Convert doctor to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.user.full_name if self.user else 'N/A',
            'email': self.user.email if self.user else 'N/A',
            'phone': self.user.phone if self.user else 'N/A',
            'specialization': self.specialization,
            'license_number': self.license_number,
            'experience_years': self.experience_years,
            'qualification': self.qualification,
            'clinic_address': self.clinic_address,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else 0,
            'available_from': self.available_from.isoformat() if self.available_from else None,
            'available_to': self.available_to.isoformat() if self.available_to else None,
            'is_available': self.is_available
        }
