# rsa_core.py
import random
import math
import hashlib

def is_prime(num):
    """
    Допоміжна функція: перевірка числа на простоту.
    Використовується метод перебору дільників (достатньо для навчального PoC).
    Для реальних промислових систем використовуються тести Міллера-Рабіна тощо.
    """
    if num < 2:
        return False
    # Перевіряємо дільники лише до квадратного кореня з числа
    for i in range(2, int(math.isqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime(min_val=100, max_val=1000):
    """
    Генерує випадкове просте число у заданому діапазоні.
    Використовується для знаходження параметрів 'p' та 'q'.
    """
    prime = random.randint(min_val, max_val)
    while not is_prime(prime):
        prime = random.randint(min_val, max_val)
    return prime

def extended_gcd(a, b):
    """
    Розширений алгоритм Евкліда.
    Повертає кортеж (g, x, y), де g - найбільший спільний дільник (НСД),
    а x та y - коефіцієнти рівняння Безу (ax + by = g).
    """
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

def mod_inverse(e, phi):
    """
    Обчислення мультиплікативного оберненого елемента за модулем.
    Необхідно для знаходження закритої експоненти 'd', такої що: (e * d) mod phi = 1.
    """
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Оберненого елемента не існує (числа не взаємно прості).")
    return x % phi

def generate_keypair(min_val=1000, max_val=5000):
    """
    Генерація пари ключів RSA (Відкритого та Закритого).
    """
    # 1. Вибираємо два великих простих числа p та q
    p = generate_prime(min_val, max_val)
    q = generate_prime(min_val, max_val)
    while p == q: # Гарантуємо, що p і q - різні
        q = generate_prime(min_val, max_val)
        
    # 2. Обчислюємо модуль n (системний модуль)
    n = p * q
    
    # 3. Обчислюємо функцію Ейлера phi(n)
    phi = (p - 1) * (q - 1)
    
    # 4. Вибираємо відкриту експоненту e, яка взаємно проста з phi
    # Часто на практиці використовують прості числа Ферма, напр. 65537
    e = random.randrange(2, phi)
    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(2, phi)
        g = math.gcd(e, phi)
        
    # 5. Обчислюємо закриту експоненту d
    d = mod_inverse(e, phi)
    
    # Відкритий ключ: (e, n), Закритий ключ: (d, n)
    return ((e, n), (d, n))

def hash_message(message):
    """
    Реалізація гешування повідомлення алгоритмом SHA-256.
    Повертає ціле число (int), зручне для математичних операцій RSA.
    """
    # Перетворюємо рядок у байти та гешуємо
    sha_signature = hashlib.sha256(message.encode('utf-8')).hexdigest()
    # Конвертуємо шістнадцятковий результат у десяткове число
    return int(sha_signature, 16)

def sign_message(message, private_key):
    """
    Процедура створення електронного цифрового підпису (ЕЦП).
    S = (H(m)^d) mod n
    """
    d, n = private_key
    # Обчислюємо геш повідомлення
    h = hash_message(message)
    # Зменшуємо геш за модулем n (щоб його можна було піднести до степеня в кільці вирахувань n)
    h_mod = h % n 
    # Піднесення до степеня за модулем (Square-and-Multiply оптимізовано в Python)
    signature = pow(h_mod, d, n)
    return signature

def verify_signature(message, signature, public_key):
    """
    Процедура верифікації (перевірки) ЕЦП.
    H(m) == (S^e) mod n
    """
    e, n = public_key
    # Знову знаходимо геш оригінального повідомлення
    h = hash_message(message)
    h_mod = h % n
    
    # Розшифровуємо підпис за допомогою відкритого ключа
    h_decrypted = pow(signature, e, n)
    
    # Якщо геші співпадають — підпис валідний
    return h_mod == h_decrypted

def run_demo():
    """
    Інтерактивна демонстрація роботи базового алгоритму RSA для головного меню.
    """
    print("-" * 50)
    print("Генеруємо ключі RSA (це може зайняти мить)...")
    try:
        public_key, private_key = generate_keypair()
        print(f"[+] Відкритий ключ (e, n): {public_key}")
        print(f"[+] Закритий ключ (d, n): {private_key}")
        
        message = input("\nВведіть текстове повідомлення для підписання: ")
        if not message:
            message = "Тестове повідомлення для диплому Карп'яка Павла"
            print(f"Використано повідомлення за замовчуванням: '{message}'")
            
        print("\n--- Процес Підписання ---")
        signature = sign_message(message, private_key)
        print(f"Згенерований цифровий підпис: {signature}")
        
        print("\n--- Процес Верифікації ---")
        is_valid = verify_signature(message, signature, public_key)
        
        if is_valid:
            print("[+] Верифікація УСПІШНА! Підпис справжній.")
        else:
            print("[-] Верифікація ПРОВАЛЕНА! Підпис підроблено або повідомлення змінено.")
            
        print("-" * 50)
        input("\nНатисніть Enter, щоб повернутися до головного меню...")
        
    except Exception as e:
         print(f"\n[!] Сталася помилка у модулі rsa_core: {e}")