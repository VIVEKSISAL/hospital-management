"""
Routes/Blueprints for Hospital Management System
"""
from flask import Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .patient import patient_bp
from .doctor import doctor_bp
from .appointment import appointment_bp
from .billing import billing_bp
from .room import room_bp
from .lab_report import lab_report_bp

__all__ = [
    'auth_bp',
    'dashboard_bp',
    'patient_bp',
    'doctor_bp',
    'appointment_bp',
    'billing_bp',
    'room_bp',
    'lab_report_bp'
]
