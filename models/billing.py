"""
Billing model for billing management
"""
from datetime import datetime
from . import db

class Billing(db.Model):
    """Billing model for managing patient bills"""
    __tablename__ = 'billing'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), 
                          nullable=False, index=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='SET NULL'), 
                              nullable=True)
    billing_date = db.Column(db.Date, nullable=False, index=True)
    consultation_fee = db.Column(db.DECIMAL(10, 2), default=0)
    medicine_cost = db.Column(db.DECIMAL(10, 2), default=0)
    test_cost = db.Column(db.DECIMAL(10, 2), default=0)
    room_cost = db.Column(db.DECIMAL(10, 2), default=0)
    other_charges = db.Column(db.DECIMAL(10, 2), default=0)
    discount = db.Column(db.DECIMAL(10, 2), default=0)
    amount_paid = db.Column(db.DECIMAL(10, 2), default=0)
    payment_status = db.Column(db.Enum('Unpaid', 'Partial', 'Paid'), 
                              default='Unpaid', index=True)
    payment_method = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Billing {self.id} - Patient {self.patient_id}>'
    
    def get_total_amount(self):
        """Calculate total amount"""
        total = float(self.consultation_fee or 0) + float(self.medicine_cost or 0) + \
                float(self.test_cost or 0) + float(self.room_cost or 0) + \
                float(self.other_charges or 0)
        return total
    
    def get_amount_due(self):
        """Calculate amount due"""
        total = self.get_total_amount()
        discount = float(self.discount or 0)
        amount_paid = float(self.amount_paid or 0)
        return total - discount - amount_paid
    
    def is_paid(self):
        """Check if bill is fully paid"""
        return self.get_amount_due() <= 0
    
    def is_unpaid(self):
        """Check if bill is unpaid"""
        return self.payment_status == 'Unpaid' and float(self.amount_paid or 0) == 0
    
    def is_partial(self):
        """Check if bill is partially paid"""
        return self.payment_status == 'Partial'
    
    def calculate_payment_status(self):
        """Calculate and update payment status"""
        amount_due = self.get_amount_due()
        if amount_due <= 0:
            self.payment_status = 'Paid'
        elif float(self.amount_paid or 0) > 0:
            self.payment_status = 'Partial'
        else:
            self.payment_status = 'Unpaid'
    
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
    
    def to_dict(self):
        """Convert billing to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'appointment_id': self.appointment_id,
            'patient': self.get_patient_info(),
            'billing_date': self.billing_date.isoformat() if self.billing_date else None,
            'consultation_fee': float(self.consultation_fee or 0),
            'medicine_cost': float(self.medicine_cost or 0),
            'test_cost': float(self.test_cost or 0),
            'room_cost': float(self.room_cost or 0),
            'other_charges': float(self.other_charges or 0),
            'total_amount': self.get_total_amount(),
            'discount': float(self.discount or 0),
            'amount_paid': float(self.amount_paid or 0),
            'amount_due': self.get_amount_due(),
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'notes': self.notes
        }
