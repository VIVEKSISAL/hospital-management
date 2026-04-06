"""
Database models for Hospital Management System
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .patient import Patient
from .doctor import Doctor
from .appointment import Appointment
from .room import Room
from .room_allocation import RoomAllocation
from .lab_report import LabReport
from .billing import Billing
from .medicine import Medicine
from .prescription import Prescription

__all__ = [
    'db',
    'User',
    'Patient',
    'Doctor',
    'Appointment',
    'Room',
    'RoomAllocation',
    'LabReport',
    'Billing',
    'Medicine',
    'Prescription'
]
