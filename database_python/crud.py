from models.hospital import db, Department, Doctor, Patient, Appointment, Prescription, Gender
from datetime import datetime
from typing import List, Optional

class BaseCRUD:
    @staticmethod
    def add_and_commit(item):
        try:
            db.session.add(item)
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_and_commit(item):
        try:
            db.session.delete(item)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

class DepartmentCRUD(BaseCRUD):
    @staticmethod
    def create(name: str, floor_number: int) -> Department:
        department = Department(name=name, floor_number=floor_number)
        return BaseCRUD.add_and_commit(department)

    @staticmethod
    def get(department_id: int) -> Optional[Department]:
        return Department.query.get_or_404(department_id)

    @staticmethod
    def get_all() -> List[Department]:
        return Department.query.all()

    @staticmethod
    def update(department_id: int, **kwargs) -> Department:
        department = DepartmentCRUD.get(department_id)
        for key, value in kwargs.items():
            setattr(department, key, value)
        return BaseCRUD.add_and_commit(department)

    @staticmethod
    def delete(department_id: int) -> bool:
        department = DepartmentCRUD.get(department_id)
        return BaseCRUD.delete_and_commit(department)

class DoctorCRUD(BaseCRUD):
    @staticmethod
    def create(first_name: str, last_name: str, specialty: str,
              phone_number: str, email: str, department_id: int) -> Doctor:
        doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            specialty=specialty,
            phone_number=phone_number,
            email=email,
            department_id=department_id
        )
        return BaseCRUD.add_and_commit(doctor)

    @staticmethod
    def get(doctor_id: int) -> Optional[Doctor]:
        return Doctor.query.get_or_404(doctor_id)

    @staticmethod
    def get_all() -> List[Doctor]:
        return Doctor.query.all()

    @staticmethod
    def get_by_department(department_id: int) -> List[Doctor]:
        return Doctor.query.filter_by(department_id=department_id).all()

    @staticmethod
    def update(doctor_id: int, **kwargs) -> Doctor:
        doctor = DoctorCRUD.get(doctor_id)
        for key, value in kwargs.items():
            setattr(doctor, key, value)
        return BaseCRUD.add_and_commit(doctor)

    @staticmethod
    def delete(doctor_id: int) -> bool:
        doctor = DoctorCRUD.get(doctor_id)
        return BaseCRUD.delete_and_commit(doctor)

class PatientCRUD(BaseCRUD):
    @staticmethod
    def create(first_name: str, last_name: str, date_of_birth: datetime,
              gender: Gender, phone_number: str, address: str, email: str) -> Patient:
        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number,
            address=address,
            email=email
        )
        return BaseCRUD.add_and_commit(patient)

    @staticmethod
    def get(patient_id: int) -> Optional[Patient]:
        return Patient.query.get_or_404(patient_id)

    @staticmethod
    def get_all() -> List[Patient]:
        return Patient.query.all()

    @staticmethod
    def update(patient_id: int, **kwargs) -> Patient:
        patient = PatientCRUD.get(patient_id)
        for key, value in kwargs.items():
            setattr(patient, key, value)
        return BaseCRUD.add_and_commit(patient)

    @staticmethod
    def delete(patient_id: int) -> bool:
        patient = PatientCRUD.get(patient_id)
        return BaseCRUD.delete_and_commit(patient)

class AppointmentCRUD(BaseCRUD):
    @staticmethod
    def create(patient_id: int, doctor_id: int,
              appointment_datetime: datetime, reason_for_visit: str) -> Appointment:
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_datetime=appointment_datetime,
            reason_for_visit=reason_for_visit
        )
        return BaseCRUD.add_and_commit(appointment)

    @staticmethod
    def get(appointment_id: int) -> Optional[Appointment]:
        return Appointment.query.get_or_404(appointment_id)

    @staticmethod
    def get_all() -> List[Appointment]:
        return Appointment.query.all()

    @staticmethod
    def get_by_doctor(doctor_id: int) -> List[Appointment]:
        return Appointment.query.filter_by(doctor_id=doctor_id).all()

    @staticmethod
    def get_by_patient(patient_id: int) -> List[Appointment]:
        return Appointment.query.filter_by(patient_id=patient_id).all()

    @staticmethod
    def update(appointment_id: int, **kwargs) -> Appointment:
        appointment = AppointmentCRUD.get(appointment_id)
        for key, value in kwargs.items():
            setattr(appointment, key, value)
        return BaseCRUD.add_and_commit(appointment)

    @staticmethod
    def delete(appointment_id: int) -> bool:
        appointment = AppointmentCRUD.get(appointment_id)
        return BaseCRUD.delete_and_commit(appointment)

class PrescriptionCRUD(BaseCRUD):
    @staticmethod
    def create(patient_id: int, doctor_id: int, medication_name: str,
              dosage: str, frequency: str, start_date: datetime,
              end_date: datetime) -> Prescription:
        prescription = Prescription(
            patient_id=patient_id,
            doctor_id=doctor_id,
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date
        )
        return BaseCRUD.add_and_commit(prescription)

    @staticmethod
    def get(prescription_id: int) -> Optional[Prescription]:
        return Prescription.query.get_or_404(prescription_id)

    @staticmethod
    def get_all() -> List[Prescription]:
        return Prescription.query.all()

    @staticmethod
    def get_by_patient(patient_id: int) -> List[Prescription]:
        return Prescription.query.filter_by(patient_id=patient_id).all()

    @staticmethod
    def get_by_doctor(doctor_id: int) -> List[Prescription]:
        return Prescription.query.filter_by(doctor_id=doctor_id).all()

    @staticmethod
    def update(prescription_id: int, **kwargs) -> Prescription:
        prescription = PrescriptionCRUD.get(prescription_id)
        for key, value in kwargs.items():
            setattr(prescription, key, value)
        return BaseCRUD.add_and_commit(prescription)

    @staticmethod
    def delete(prescription_id: int) -> bool:
        prescription = PrescriptionCRUD.get(prescription_id)
        return BaseCRUD.delete_and_commit(prescription)

# Фасад для зручного доступу до всіх CRUD операцій
class CRUDOperations:
    department = DepartmentCRUD
    doctor = DoctorCRUD
    patient = PatientCRUD
    appointment = AppointmentCRUD
    prescription = PrescriptionCRUD

    # Методи-помічники для сумісності зі старим кодом
    @staticmethod
    def create_department(*args, **kwargs):
        return DepartmentCRUD.create(*args, **kwargs)

    @staticmethod
    def get_department(*args, **kwargs):
        return DepartmentCRUD.get(*args, **kwargs)

    @staticmethod
    def update_department(*args, **kwargs):
        return DepartmentCRUD.update(*args, **kwargs)

    @staticmethod
    def delete_department(*args, **kwargs):
        return DepartmentCRUD.delete(*args, **kwargs)

    @staticmethod
    def create_doctor(*args, **kwargs):
        return DoctorCRUD.create(*args, **kwargs)

    @staticmethod
    def get_doctor(*args, **kwargs):
        return DoctorCRUD.get(*args, **kwargs)

    @staticmethod
    def delete_doctor(*args, **kwargs):
        return DoctorCRUD.delete(*args, **kwargs)

    @staticmethod
    def create_patient(*args, **kwargs):
        return PatientCRUD.create(*args, **kwargs)

    @staticmethod
    def get_patient(*args, **kwargs):
        return PatientCRUD.get(*args, **kwargs)

    @staticmethod
    def delete_patient(*args, **kwargs):
        return PatientCRUD.delete(*args, **kwargs)

    @staticmethod
    def create_appointment(*args, **kwargs):
        return AppointmentCRUD.create(*args, **kwargs)

    @staticmethod
    def get_appointment(*args, **kwargs):
        return AppointmentCRUD.get(*args, **kwargs)

    @staticmethod
    def delete_appointment(*args, **kwargs):
        return AppointmentCRUD.delete(*args, **kwargs)

    @staticmethod
    def create_prescription(*args, **kwargs):
        return PrescriptionCRUD.create(*args, **kwargs)

    @staticmethod
    def get_prescription(*args, **kwargs):
        return PrescriptionCRUD.get(*args, **kwargs)

    @staticmethod
    def delete_prescription(*args, **kwargs):
        return PrescriptionCRUD.delete(*args, **kwargs)

    @staticmethod
    def get_all_departments():
        return DepartmentCRUD.get_all()

    @staticmethod
    def get_all_doctors():
        return DoctorCRUD.get_all()

    @staticmethod
    def get_all_patients():
        return PatientCRUD.get_all()

    @staticmethod
    def get_all_appointments():
        return AppointmentCRUD.get_all()

    @staticmethod
    def get_all_prescriptions():
        return PrescriptionCRUD.get_all()

    @staticmethod
    def find_doctors_by_department(department_id: int):
        return DoctorCRUD.get_by_department(department_id)

    @staticmethod
    def find_appointments_by_doctor(doctor_id: int):
        return AppointmentCRUD.get_by_doctor(doctor_id)

    @staticmethod
    def find_appointments_by_patient(patient_id: int):
        return AppointmentCRUD.get_by_patient(patient_id)

    @staticmethod
    def find_prescriptions_by_patient(patient_id: int):
        return PrescriptionCRUD.get_by_patient(patient_id) 