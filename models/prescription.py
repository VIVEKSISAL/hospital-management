"""
Prescription model for medicine prescriptions
"""
from datetime import datetime
from . import db

class Prescription(db.Model):
    """Prescription model for storing medicine prescriptions"""
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), 
                              nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), 
                          nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), 
                         nullable=False)
    prescription_date = db.Column(db.Date, nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id', ondelete='SET NULL'), 
                           nullable=True)
    medicine_name = db.Column(db.String(150))
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    duration_unit = db.Column(db.Enum('Days', 'Weeks', 'Months'), default='Days')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prescription {self.medicine_name} - {self.prescription_date}>'
    
    def get_medicine_cost(self):
        """Get cost of prescribed medicine"""
        if self.medicine and self.medicine.unit_price:
            # Estimate cost based on dose frequency
            # This is a simple calculation, adjust based on your logic
            return float(self.medicine.unit_price)
        return 0
    
    def get_duration_in_days(self):
        """Get duration in days"""
        if self.duration_unit == 'Weeks':
            return self.duration * 7
        elif self.duration_unit == 'Months':
            return self.duration * 30
        else:
            return self.duration
    
    def get_prescription_display(self):
        """Get prescription display string"""
        return f"{self.medicine_name} - {self.dosage}, {self.frequency} for {self.duration} {self.duration_unit}"
    
    def get_doctor_info(self):
        """Get doctor information"""
        if self.doctor and self.doctor.user:
            return {
                'id': self.doctor.id,
                'name': self.doctor.user.full_name,
                'specialization': self.doctor.specialization
            }
        return None
    
    def get_patient_info(self):
        """Get patient information"""
        if self.patient and self.patient.user:
            return {
                'id': self.patient.id,
                'name': self.patient.user.full_name
            }
        return None
    
    def to_dict(self):
        """Convert prescription to dictionary"""
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient': self.get_patient_info(),
            'doctor': self.get_doctor_info(),
            'prescription_date': self.prescription_date.isoformat() if self.prescription_date else None,
            'medicine_id': self.medicine_id,
            'medicine_name': self.medicine_name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'duration': self.duration,
            'duration_unit': self.duration_unit,
            'prescription_display': self.get_prescription_display(),
            'notes': self.notes
        }
