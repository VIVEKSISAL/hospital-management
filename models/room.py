"""
Room model for room/ward management
"""
from datetime import datetime
from . import db

class Room(db.Model):
    """Room model for storing room/ward information"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.Enum('General', 'Semi-Private', 'Private', 'ICU'), 
                         nullable=False, index=True)
    floor = db.Column(db.Integer)
    capacity = db.Column(db.Integer, default=1)
    occupied_beds = db.Column(db.Integer, default=0)
    rate_per_day = db.Column(db.DECIMAL(10, 2))
    facilities = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    room_allocations = db.relationship('RoomAllocation', backref='room', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Room {self.room_number}>'
    
    def get_available_beds(self):
        """Get number of available beds"""
        return self.capacity - self.occupied_beds
    
    def is_full(self):
        """Check if room is full"""
        return self.occupied_beds >= self.capacity
    
    def get_occupancy_percentage(self):
        """Get occupancy percentage"""
        if self.capacity == 0:
            return 0
        return (self.occupied_beds / self.capacity) * 100
    
    def get_current_patients(self):
        """Get currently admitted patients"""
        from datetime import date
        active_allocations = [
            alloc for alloc in self.room_allocations 
            if alloc.status == 'Active' and alloc.discharge_date is None
        ]
        return active_allocations
    
    def get_patient_count(self):
        """Get current patient count"""
        return len(self.get_current_patients())
    
    def can_allocate_patient(self):
        """Check if patient can be allocated to this room"""
        return self.is_available and not self.is_full()
    
    def to_dict(self):
        """Convert room to dictionary"""
        return {
            'id': self.id,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'floor': self.floor,
            'capacity': self.capacity,
            'occupied_beds': self.occupied_beds,
            'available_beds': self.get_available_beds(),
            'occupancy_percentage': self.get_occupancy_percentage(),
            'rate_per_day': float(self.rate_per_day) if self.rate_per_day else 0,
            'facilities': self.facilities,
            'is_available': self.is_available,
            'is_full': self.is_full()
        }
