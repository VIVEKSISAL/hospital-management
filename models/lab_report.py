"""
Lab Report model for laboratory tests
"""
from datetime import datetime
from . import db

class LabReport(db.Model):
    """Lab Report model for storing laboratory test reports"""
    __tablename__ = 'lab_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), 
                          nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='SET NULL'), 
                         nullable=True)
    test_name = db.Column(db.String(150), nullable=False)
    test_type = db.Column(db.String(100))
    test_date = db.Column(db.Date, nullable=False, index=True)
    result = db.Column(db.Text)
    status = db.Column(db.Enum('Pending', 'Complete', 'Cancelled'), 
                      default='Pending', index=True)
    normal_range = db.Column(db.String(100))
    comments = db.Column(db.Text)
    cost = db.Column(db.DECIMAL(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LabReport {self.test_name} - {self.patient_id}>'
    
    def is_complete(self):
        """Check if test report is complete"""
        return self.status == 'Complete' and self.result is not None
    
    def is_pending(self):
        """Check if test is pending"""
        return self.status == 'Pending'
    
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
                'specialization': self.doctor.specialization
            }
        return None
    
    def to_dict(self):
        """Convert lab report to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient': self.get_patient_info(),
            'doctor': self.get_doctor_info(),
            'test_name': self.test_name,
            'test_type': self.test_type,
            'test_date': self.test_date.isoformat() if self.test_date else None,
            'result': self.result,
            'status': self.status,
            'normal_range': self.normal_range,
            'comments': self.comments,
            'cost': float(self.cost) if self.cost else 0
        }
