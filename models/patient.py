"""
Patient model for patient management
"""
from datetime import datetime
from . import db

class Patient(db.Model):
    """Patient model for storing patient information"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), 
                       unique=True, nullable=True)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    blood_group = db.Column(db.String(5))
    address = db.Column(db.String(255))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    emergency_contact = db.Column(db.String(15))
    emergency_contact_name = db.Column(db.String(100))
    medical_history = db.Column(db.Text)
    allergies = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', cascade='all, delete-orphan')
    lab_reports = db.relationship('LabReport', backref='patient', cascade='all, delete-orphan')
    billings = db.relationship('Billing', backref='patient', cascade='all, delete-orphan')
    room_allocations = db.relationship('RoomAllocation', backref='patient', cascade='all, delete-orphan')
    prescriptions = db.relationship('Prescription', backref='patient', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Patient {self.user.full_name if self.user else "Unknown"}>'
    
    def get_age(self):
        """Calculate patient age"""
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - \
                   ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def get_active_appointments(self):
        """Get active appointments"""
        return [apt for apt in self.appointments if apt.status in ['Scheduled', 'Completed']]
    
    def get_pending_bills(self):
        """Get unpaid bills"""
        return [bill for bill in self.billings if bill.payment_status != 'Paid']
    
    def to_dict(self):
        """Convert patient to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.user.full_name if self.user else 'N/A',
            'email': self.user.email if self.user else 'N/A',
            'phone': self.user.phone if self.user else 'N/A',
            'age': self.get_age(),
            'gender': self.gender,
            'blood_group': self.blood_group,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'emergency_contact': self.emergency_contact,
            'emergency_contact_name': self.emergency_contact_name,
            'medical_history': self.medical_history,
            'allergies': self.allergies,
            'current_medications': self.current_medications
        }
