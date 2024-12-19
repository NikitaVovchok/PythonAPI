import requests
import time
import random
from datetime import datetime, timedelta
import json
from faker import Faker
import statistics

BASE_URL = 'http://localhost:5000'
fake = Faker()

def generate_test_data(count):
    """Генерує тестові дані"""
    departments = []
    doctors = []
    patients = []
    
    # Список можливих відділень
    department_types = [
        'Cardiology', 'Neurology', 'Pediatrics', 'Surgery',
        'Orthopedics', 'Oncology', 'Emergency', 'Psychiatry'
    ]
    
    # Список можливих спеціальностей
    specialties = [
        'Cardiologist', 'Neurologist', 'Pediatrician', 'Surgeon',
        'Orthopedist', 'Oncologist', 'Emergency Physician', 'Psychiatrist'
    ]
    
    # Створюємо відділення
    for i in range(max(count // 100, 1)):  # 1 відділення на 100 записів
        departments.append({
            'name': f'Department of {random.choice(department_types)}',
            'floor_number': random.randint(1, 5)
        })
    
    # Створюємо лікарів
    for i in range(max(count // 50, 1)):  # 1 лікар на 50 записів
        doctors.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'specialty': random.choice(specialties),
            'phone_number': fake.phone_number(),
            'email': fake.email(),
            'department_id': 1  # Буде оновлено після створення відділень
        })
    
    # Створюємо пацієнтів
    for i in range(count):
        patients.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(minimum_age=10, maximum_age=90).strftime('%Y-%m-%d'),
            'gender': random.choice(['MALE', 'FEMALE']),
            'phone_number': fake.phone_number(),
            'address': fake.address(),
            'email': fake.email()
        })
    
    return departments, doctors, patients

def measure_performance(operation_name, operation_func, iterations=1):
    """Вимірює час виконання операції"""
    times = []
    for _ in range(iterations):
        start_time = time.time()
        result = operation_func()
        end_time = time.time()
        times.append(end_time - start_time)
    
    avg_time = statistics.mean(times)
    print(f"{operation_name}: {avg_time:.4f} seconds (average of {iterations} iterations)")
    return avg_time

def run_benchmark(data_size):
    print(f"\nRunning benchmark for {data_size} records...")
    
    departments, doctors, patients = generate_test_data(data_size)
    
    # Спочатку створюємо базові дані
    print("Creating initial data...")
    
    # Створюємо відділення
    for dept in departments[:1]:  # Створюємо хоча б одне відділення
        response = requests.post(f"{BASE_URL}/departments", json=dept)
        if response.status_code == 201:
            dept_id = response.json()['id']
            # Оновлюємо department_id для лікарів
            for doctor in doctors:
                doctor['department_id'] = dept_id
    
    # Створюємо одного лікаря
    for doctor in doctors[:1]:  # Створюємо хоча б одного лікаря
        requests.post(f"{BASE_URL}/doctors", json=doctor)
    
    print("Initial data created. Starting benchmarks...")
    
    # Тест INSERT
    def test_insert():
        response = requests.post(f"{BASE_URL}/patients", json=random.choice(patients))
        return response
    
    # Тест SELECT
    def test_select():
        response = requests.get(f"{BASE_URL}/patients")
        return response
    
    # Тест UPDATE (оновлюємо email випадкового пацієнта)
    def test_update():
        patients_list = requests.get(f"{BASE_URL}/patients").json()
        if patients_list:
            patient = random.choice(patients_list)
            patient['email'] = fake.email()
            response = requests.put(f"{BASE_URL}/patients/{patient['id']}", json=patient)
            return response
        return None
    
    # Тест DELETE
    def test_delete():
        patients_list = requests.get(f"{BASE_URL}/patients").json()
        if patients_list:
            patient = random.choice(patients_list)
            response = requests.delete(f"{BASE_URL}/patients/{patient['id']}")
            return response
        return None

    results = {
        'data_size': data_size,
        'insert': measure_performance('INSERT', test_insert, iterations=10),
        'select': measure_performance('SELECT', test_select, iterations=10),
        'update': measure_performance('UPDATE', test_update, iterations=10),
        'delete': measure_performance('DELETE', test_delete, iterations=10)
    }
    
    return results

def main():
    data_sizes = [1000, 10000, 100000, 1000000]
    all_results = []
    
    for size in data_sizes:
        results = run_benchmark(size)
        all_results.append(results)
        
    # Зберігаємо результати в JSON файл
    with open('benchmark_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\nResults have been saved to benchmark_results.json")

if __name__ == '__main__':
    main() 