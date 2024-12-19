import psycopg2
from config import Config
import time
from tabulate import tabulate

def test_query(query, description):
    """Тестує продуктивність запиту з EXPLAIN ANALYZE"""
    conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
    cur = conn.cursor()
    
    try:
        # Вимірюємо час звичайного виконання
        start_time = time.time()
        cur.execute(query)
        execution_time = time.time() - start_time
        
        # Отримуємо план виконання
        cur.execute(f"EXPLAIN {query}")
        plan = cur.fetchall()
        
        return {
            'description': description,
            'time': execution_time,
            'uses_index': any('Index Scan' in str(row) for row in plan),
            'plan': plan[0][0]  # Беремо перший рядок плану
        }
    
    finally:
        cur.close()
        conn.close()

def main():
    # Тестові запити
    queries = [
        (
            "SELECT * FROM patients WHERE gender = 'MALE'",
            "Пошук пацієнтів за статтю"
        ),
        (
            "SELECT * FROM doctors WHERE specialty = 'Cardiologist'",
            "Пошук лікарів за спеціальністю"
        ),
        (
            """
            SELECT a.*, p.first_name 
            FROM appointments a 
            JOIN patients p ON a.patient_id = p.id 
            WHERE DATE(appointment_datetime) = CURRENT_DATE
            """,
            "Прийоми на сьогодні"
        ),
    ]
    
    # Виконуємо тести
    results = []
    for query, description in queries:
        result = test_query(query, description)
        results.append([
            result['description'],
            f"{result['time']:.4f} сек",
            "Так" if result['uses_index'] else "Ні",
            result['plan']
        ])
    
    # Виводимо результати
    print("\nРезультати тестування:")
    print(tabulate(
        results,
        headers=['Опис', 'Час виконання', 'Використання індексу', 'План виконання'],
        tablefmt='grid'
    ))

if __name__ == '__main__':
    main() 