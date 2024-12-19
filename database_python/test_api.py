import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5000'

def test_api():
    # Створення відділення
    department_data = {
        'name': 'Кардіологія',
        'floor_number': 3
    }
    response = requests.post(f'{BASE_URL}/departments', json=department_data)
    department_id = response.json()['id']
    print("✅ Відділення створено")

    # Створення лікаря
    doctor_data = {
        'first_name': 'Іван',
        'last_name': 'Петренко',
        'specialty': 'Кардіолог',
        'phone_number': '+380991234567',
        'email': 'petrenko@hospital.com',
        'department_id': department_id
    }
    response = requests.post(f'{BASE_URL}/doctors', json=doctor_data)
    doctor_id = response.json()['id']
    print("✅ Лікаря створено")

    # Створення пацієнта
    patient_data = {
        'first_name': 'Марія',
        'last_name': 'Коваленко',
        'date_of_birth': '1990-05-15',
        'gender': 'Female',
        'phone_number': '+380997654321',
        'address': 'вул. Шевченка, 1, Київ',
        'email': 'kovalenko@gmail.com'
    }
    response = requests.post(f'{BASE_URL}/patients', json=patient_data)
    patient_id = response.json()['id']
    print("✅ Пацієнта створено")

    # Створення прийому
    appointment_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'appointment_datetime': datetime.now().isoformat(),
        'reason_for_visit': 'Регулярний огляд'
    }
    response = requests.post(f'{BASE_URL}/appointments', json=appointment_data)
    print("✅ Прийом створено")

    # Створення рецепту
    prescription_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'medication_name': 'Аспірин',
        'dosage': '100мг',
        'frequency': '1 раз на день',
        'start_date': datetime.now().date().isoformat(),
        'end_date': (datetime.now() + timedelta(days=30)).date().isoformat()
    }
    response = requests.post(f'{BASE_URL}/prescriptions', json=prescription_data)
    print("✅ Рецепт створено")

    # Перевірка GET запитів
    print("\nПеревірка даних через API:")
    print(f"Відділення: {requests.get(f'{BASE_URL}/departments').json()}")
    print(f"Лікарі: {requests.get(f'{BASE_URL}/doctors').json()}")
    print(f"Пацієнти: {requests.get(f'{BASE_URL}/patients').json()}")
    print(f"Прийоми: {requests.get(f'{BASE_URL}/appointments').json()}")
    print(f"Рецепти: {requests.get(f'{BASE_URL}/prescriptions').json()}")

if __name__ == '__main__':
    test_api() 