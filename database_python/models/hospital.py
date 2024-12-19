from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class Gender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    floor_number = db.Column(db.Integer)
    doctors = db.relationship('Doctor', backref='department', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'floor_number': self.floor_number
        }

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    prescriptions = db.relationship('Prescription', backref='doctor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'specialty': self.specialty,
            'phone_number': self.phone_number,
            'email': self.email,
            'department_id': self.department_id
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    phone_number = db.Column(db.String(15))
    address = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    prescriptions = db.relationship('Prescription', backref='patient', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat(),
            'gender': self.gender.value,
            'phone_number': self.phone_number,
            'address': self.address,
            'email': self.email
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False)
    reason_for_visit = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_datetime': self.appointment_datetime.isoformat(),
            'reason_for_visit': self.reason_for_visit
        }

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'medication_name': self.medication_name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat()
        } 