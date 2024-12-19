from flask import Flask
from models.hospital import db, Gender
from crud import CRUDOperations
from config import Config
from datetime import datetime, date, timedelta
import random

def generate_random_phone():
    return f"+38099{random.randint(1000000, 9999999)}"

def generate_random_email(name):
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    return f"{name.lower()}{random.randint(1, 999)}@{random.choice(domains)}"

def generate_random_date(start_year=1950, end_year=2000):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)

def get_random_name(is_male=True):
    male_names = ['Іван', 'Петро', 'Михайло', 'Андрій', 'Олександр', 'Василь', 'Сергій']
    female_names = ['Марія', 'Олена', 'Анна', 'Ірина', 'Тетяна', 'Наталія', 'Юлія']
    male_surnames = ['Петренко', 'Коваленко', 'Бондаренко', 'Шевченко', 'Мельник', 'Ткаченко']
    female_surnames = ['Петренко', 'Коваленко', 'Бондаренко', 'Шевченко', 'Мельник', 'Ткаченко']
    
    if is_male:
        return random.choice(male_names), random.choice(male_surnames)
    return random.choice(female_names), random.choice(female_surnames)

def get_random_department():
    departments = [
        ('Кардіологія', 2),
        ('Неврологія', 3),
        ('Педіатрія', 1),
        ('Хірургія', 4),
        ('Терапія', 2),
        ('Ортопедія', 3),
        ('Офтальмологія', 1)
    ]
    return random.choice(departments)

def get_random_specialty():
    specialties = [
        'Кардіолог', 'Невролог', 'Педіатр', 'Хірург', 
        'Терапевт', 'Ортопед', 'Офтальмолог'
    ]
    return random.choice(specialties)

def get_random_reason():
    reasons = [
        'Головний біль', 'Біль у спині', 'Регулярний огляд',
        'Консультація', 'Високий тиск', 'Болі в суглобах',
        'Застуда', 'Алергія', 'Профілактичний огляд'
    ]
    return random.choice(reasons)

def get_random_medication():
    medications = [
        ('Аспірин', '100мг', '1 раз на день'),
        ('Парацетамол', '500мг', '3 рази на день'),
        ('Ібупрофен', '200мг', '2 рази на день'),
        ('Амоксицилін', '250мг', '2 рази на день'),
        ('Омепразол', '20мг', '1 раз на день'),
        ('Лоратадин', '10мг', '1 раз на день')
    ]
    return random.choice(medications)

def test_crud_operations():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            print("✅ Таблиці створено успішно")

            # Створення декількох відділень
            departments = []
            for _ in range(random.randint(2, 5)):
                dept_name, floor = get_random_department()
                department = CRUDOperations.create_department(
                    name=f"{dept_name}_{random.randint(1, 100)}", # Додаємо унікальний номер
                    floor_number=floor
                )
                departments.append(department)
                print(f"✅ Створено відділення: {department.name} на {floor} поверсі")

            # Створення декількох лікарів
            doctors = []
            for department in departments:
                for _ in range(random.randint(1, 3)):
                    doctor_first_name, doctor_last_name = get_random_name(is_male=random.choice([True, False]))
                    doctor = CRUDOperations.create_doctor(
                        first_name=doctor_first_name,
                        last_name=doctor_last_name,
                        specialty=get_random_specialty(),
                        phone_number=generate_random_phone(),
                        email=generate_random_email(f"{doctor_first_name}_{doctor_last_name}_{random.randint(1, 999)}"),
                        department_id=department.id
                    )
                    doctors.append(doctor)
                    print(f"✅ Створено лікаря: {doctor_first_name} {doctor_last_name}")

            # Створення декількох пацієнтів
            patients = []
            for _ in range(random.randint(3, 7)):
                is_male = random.choice([True, False])
                patient_first_name, patient_last_name = get_random_name(is_male=is_male)
                patient = CRUDOperations.create_patient(
                    first_name=patient_first_name,
                    last_name=patient_last_name,
                    date_of_birth=generate_random_date(),
                    gender=Gender.MALE if is_male else Gender.FEMALE,
                    phone_number=generate_random_phone(),
                    address=f'вул. {random.choice(["Шевченка", "Франка", "Лесі Українки", "Сагайдачного"])}, {random.randint(1, 100)}, Київ',
                    email=generate_random_email(f"{patient_first_name}_{patient_last_name}_{random.randint(1, 999)}")
                )
                patients.append(patient)
                print(f"✅ Створено пацієнта: {patient_first_name} {patient_last_name}")

            # Створення декількох прийомів
            appointments = []
            for patient in patients:
                for _ in range(random.randint(1, 3)):
                    doctor = random.choice(doctors)
                    appointment = CRUDOperations.create_appointment(
                        patient_id=patient.id,
                        doctor_id=doctor.id,
                        appointment_datetime=datetime.now() + timedelta(days=random.randint(1, 30)),
                        reason_for_visit=get_random_reason()
                    )
                    appointments.append(appointment)
                    print(f"✅ Створено прийом: Пацієнт {patient.last_name} до лікаря {doctor.last_name}")

            # Створення декількох рецептів
            prescriptions = []
            for appointment in appointments:
                if random.choice([True, False]):  # 50% ймовірність створення рецепту
                    med_name, dosage, frequency = get_random_medication()
                    prescription = CRUDOperations.create_prescription(
                        patient_id=appointment.patient_id,
                        doctor_id=appointment.doctor_id,
                        medication_name=med_name,
                        dosage=dosage,
                        frequency=frequency,
                        start_date=date.today(),
                        end_date=date.today() + timedelta(days=random.randint(7, 30))
                    )
                    prescriptions.append(prescription)
                    print(f"✅ Створено рецепт: {med_name} {dosage}")

            # Статистика
            print("\n📊 Статистика тестової бази даних:")
            print(f"Створено відділень: {len(departments)}")
            print(f"Створено лікарів: {len(doctors)}")
            print(f"Створено пацієнтів: {len(patients)}")
            print(f"Створено прийомів: {len(appointments)}")
            print(f"Створено рецептів: {len(prescriptions)}")

            # Тестування пошуку для випадкового відділення
            test_dept = random.choice(departments)
            doctors = CRUDOperations.find_doctors_by_department(test_dept.id)
            print(f"\n✅ Знайдено лікарів у відділенні {test_dept.name}: {len(doctors)}")

            # Тестування пошуку для випадкового лікаря
            test_doctor = random.choice(doctors)
            appointments = CRUDOperations.find_appointments_by_doctor(test_doctor.id)
            print(f"✅ Знайдено прийомів у лікаря {test_doctor.last_name}: {len(appointments)}")

            # Тестування пошуку для випадкового пацієнта
            test_patient = random.choice(patients)
            prescriptions = CRUDOperations.find_prescriptions_by_patient(test_patient.id)
            print(f"✅ Знайдено рецептів пацієнта {test_patient.last_name}: {len(prescriptions)}")

            # Видалення всіх даних в правильному порядку
            print("\n🗑 Видалення даних...")
            
            # Спочатку видаляємо рецепти
            for prescription in prescriptions:
                try:
                    CRUDOperations.delete_prescription(prescription.id)
                    print(f"✓ Видалено рецепт {prescription.id}")
                except Exception as e:
                    print(f"❌ Помилка при видаленні рецепту {prescription.id}: {str(e)}")

            # Потім видаляємо прийоми
            for appointment in appointments:
                try:
                    CRUDOperations.delete_appointment(appointment.id)
                    print(f"✓ Видалено прийом {appointment.id}")
                except Exception as e:
                    print(f"❌ Помилка при видаленні прийому {appointment.id}: {str(e)}")

            # Видаляємо пацієнтів
            for patient in patients:
                try:
                    CRUDOperations.delete_patient(patient.id)
                    print(f"✓ Видалено пацієнта {patient.first_name} {patient.last_name}")
                except Exception as e:
                    print(f"❌ Помилка при видаленні пацієнта {patient.id}: {str(e)}")

            # Видаляємо лікарів
            for doctor in doctors:
                try:
                    CRUDOperations.delete_doctor(doctor.id)
                    print(f"✓ Видалено лікаря {doctor.first_name} {doctor.last_name}")
                except Exception as e:
                    print(f"❌ Помилка при видаленні лікаря {doctor.id}: {str(e)}")

            # Нарешті видаляємо відділення
            for department in departments:
                try:
                    CRUDOperations.delete_department(department.id)
                    print(f"✓ Видалено відділення {department.name}")
                except Exception as e:
                    print(f"❌ Помилка при видаленні відділення {department.id}: {str(e)}")

            print("\n✅ Всі тестові дані видалено")

            print("\n🎉 Всі CRUD тести пройдені успішно!")

        except Exception as e:
            print(f"\n❌ Помилка при тестуванні CRUD операцій: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    test_crud_operations() 