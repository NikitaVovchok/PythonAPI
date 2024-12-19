from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from models.hospital import (
    db, Department, Doctor, Patient, 
    Appointment, Prescription, Gender
)
from models.user import User
from config import Config
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)

# Зберігаємо відкликані токени
BLOCKLIST = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

# Маршрути автентифікації
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400
        
    user = User(username=data['username'])
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

# Створення таблиць
with app.app_context():
    db.create_all()

# Маршрути для Department
@app.route('/departments', methods=['POST'])
@jwt_required()
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
@jwt_required()
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

@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if key == 'date_of_birth':
                value = datetime.strptime(value, '%Y-%m-%d').date()
            if key == 'gender':
                value = Gender(value)
            setattr(patient, key, value)
            
        db.session.commit()
        return jsonify(patient.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    try:
        db.session.delete(patient)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

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
