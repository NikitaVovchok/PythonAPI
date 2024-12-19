from flask import Flask, request, jsonify
from models.hospital import (
    db, Department, Doctor, Patient, 
    Appointment, Prescription, Gender
)
from config import Config
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Створення таблиць
with app.app_context():
    db.create_all()

# Маршрути для Department
@app.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json()
    department = Department(
        name=data['name'],
        floor_number=data['floor_number']
    )
    try:
        db.session.add(department)
        db.session.commit()
        return jsonify(department.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments])

# Маршрути для Doctor
@app.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json()
    doctor = Doctor(
        first_name=data['first_name'],
        last_name=data['last_name'],
        specialty=data['specialty'],
        phone_number=data['phone_number'],
        email=data['email'],
        department_id=data['department_id']
    )
    try:
        db.session.add(doctor)
        db.session.commit()
        return jsonify(doctor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([doc.to_dict() for doc in doctors])

# Маршрути для Patient
@app.route('/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    patient = Patient(
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
        gender=Gender(data['gender']),
        phone_number=data['phone_number'],
        address=data['address'],
        email=data['email']
    )
    try:
        db.session.add(patient)
        db.session.commit()
        return jsonify(patient.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

# Маршрути для Appointment
@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appointment_datetime=datetime.fromisoformat(data['appointment_datetime']),
        reason_for_visit=data['reason_for_visit']
    )
    try:
        db.session.add(appointment)
        db.session.commit()
        return jsonify(appointment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([apt.to_dict() for apt in appointments])

# Маршрути для Prescription
@app.route('/prescriptions', methods=['POST'])
def create_prescription():
    data = request.get_json()
    prescription = Prescription(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        medication_name=data['medication_name'],
        dosage=data['dosage'],
        frequency=data['frequency'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    )
    try:
        db.session.add(prescription)
        db.session.commit()
        return jsonify(prescription.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify([pres.to_dict() for pres in prescriptions])

if __name__ == '__main__':
    app.run(debug=True)
