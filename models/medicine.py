"""
Medicine model for medicine inventory
"""
from datetime import datetime
from . import db

class Medicine(db.Model):
    """Medicine model for storing medicine information"""
    __tablename__ = 'medicines'
    
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text)
    dosage = db.Column(db.String(50))
    unit_price = db.Column(db.DECIMAL(10, 2))
    stock_quantity = db.Column(db.Integer, default=0)
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prescriptions = db.relationship('Prescription', backref='medicine', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Medicine {self.medicine_name}>'
    
    def is_in_stock(self):
        """Check if medicine is in stock"""
        return self.stock_quantity > 0
    
    def is_expired(self):
        """Check if medicine is expired"""
        from datetime import date
        if self.expiry_date:
            return date.today() > self.expiry_date
        return False
    
    def is_available_for_sale(self):
        """Check if medicine is available for sale"""
        return self.is_in_stock() and not self.is_expired()
    
    def get_stock_status(self):
        """Get stock status"""
        if self.stock_quantity == 0:
            return 'Out of Stock'
        elif self.stock_quantity < 10:
            return 'Low Stock'
        elif self.is_expired():
            return 'Expired'
        else:
            return 'Available'
    
    def update_stock(self, quantity, action='add'):
        """Update medicine stock"""
        if action == 'add':
            self.stock_quantity += quantity
        elif action == 'reduce':
            self.stock_quantity = max(0, self.stock_quantity - quantity)
    
    def to_dict(self):
        """Convert medicine to dictionary"""
        from datetime import date
        return {
            'id': self.id,
            'medicine_name': self.medicine_name,
            'description': self.description,
            'dosage': self.dosage,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'stock_quantity': self.stock_quantity,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'is_in_stock': self.is_in_stock(),
            'is_expired': self.is_expired(),
            'stock_status': self.get_stock_status()
        }
