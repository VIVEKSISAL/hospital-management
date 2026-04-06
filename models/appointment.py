"""
Appointment model for appointment management
"""
from datetime import datetime
from . import db

class Appointment(db.Model):
    """Appointment model for storing appointment information"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), 
                          nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), 
                         nullable=False, index=True)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum('Scheduled', 'Completed', 'Cancelled', 'No-Show'), 
                      default='Scheduled', index=True)
    reason_for_visit = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    billings = db.relationship('Billing', backref='appointment', cascade='all, delete-orphan')
    prescriptions = db.relationship('Prescription', backref='appointment', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'appointment_date', 'appointment_time', 
                           name='unique_appointment'),
    )
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date} {self.appointment_time}>'
    
    def get_appointment_datetime(self):
        """Get combined datetime"""
        from datetime import datetime as dt
        return dt.combine(self.appointment_date, self.appointment_time)
    
    def is_past(self):
        """Check if appointment is in the past"""
        from datetime import datetime as dt
        return self.get_appointment_datetime() < dt.now()
    
    def is_upcoming(self):
        """Check if appointment is upcoming"""
        return not self.is_past() and self.status == 'Scheduled'
    
    def can_be_cancelled(self):
        """Check if appointment can be cancelled"""
        return self.status in ['Scheduled'] and not self.is_past()
    
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
    
    def get_doctor_info(self):
        """Get doctor information"""
        if self.doctor and self.doctor.user:
            return {
                'id': self.doctor.id,
                'name': self.doctor.user.full_name,
                'specialization': self.doctor.specialization,
                'email': self.doctor.user.email,
                'phone': self.doctor.user.phone
            }
        return None
    
    def to_dict(self):
        """Convert appointment to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient': self.get_patient_info(),
            'doctor': self.get_doctor_info(),
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time.isoformat() if self.appointment_time else None,
            'status': self.status,
            'reason_for_visit': self.reason_for_visit,
            'notes': self.notes
        }
