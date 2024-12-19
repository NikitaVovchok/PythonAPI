from flask import Flask
from models.hospital import db, Department, Doctor, Patient, Appointment, Prescription, Gender
from config import Config
from datetime import datetime, date

def test_database():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        try:
            # Створюємо всі таблиці
            db.create_all()
            print("✅ Таблиці створено успішно")

            # Тестуємо створення відділення
            department = Department(
                name='Кардіологія',
                floor_number=3
            )
            db.session.add(department)
            db.session.commit()
            print("✅ Відділення створено успішно")

            # Тестуємо створення лікаря
            doctor = Doctor(
                first_name='Іван',
                last_name='Петренко',
                specialty='Кардіолог',
                phone_number='+380991234567',
                email='petrenko@hospital.com',
                department_id=department.id
            )
            db.session.add(doctor)
            db.session.commit()
            print("✅ Лікаря створено успішно")

            # Тестуємо створення пацієнта
            patient = Patient(
                first_name='Марія',
                last_name='Коваленко',
                date_of_birth=date(1990, 5, 15),
                gender=Gender.FEMALE,
                phone_number='+380997654321',
                address='вул. Шевченка, 1, Київ',
                email='kovalenko@gmail.com'
            )
            db.session.add(patient)
            db.session.commit()
            print("✅ Пацієнта створено успішно")

            # Тестуємо створення прийому
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=doctor.id,
                appointment_datetime=datetime.now(),
                reason_for_visit='Регулярний огляд'
            )
            db.session.add(appointment)
            db.session.commit()
            print("✅ Прийом створено успішно")

            # Тестуємо створення рецепту
            prescription = Prescription(
                patient_id=patient.id,
                doctor_id=doctor.id,
                medication_name='Аспірин',
                dosage='100мг',
                frequency='1 раз на день',
                start_date=date.today(),
                end_date=date(2024, 12, 31)
            )
            db.session.add(prescription)
            db.session.commit()
            print("✅ Рецепт створено успішно")

            # Тестуємо читання даних
            print("\nПеревірка даних у базі:")
            print(f"Відділення: {Department.query.all()}")
            print(f"Лікарі: {Doctor.query.all()}")
            print(f"Пацієнти: {Patient.query.all()}")
            print(f"Прийоми: {Appointment.query.all()}")
            print(f"Рецепти: {Prescription.query.all()}")

            print("\n🎉 Всі тести пройдені успішно! База даних працює коректно!")

        except Exception as e:
            print(f"\n❌ Помилка при тестуванні бази даних: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    test_database() 