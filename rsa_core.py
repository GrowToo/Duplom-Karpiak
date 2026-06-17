# rsa_core.py
import random
import math
import hashlib
import time

def is_prime(num):
    """Перевірка числа на простоту методом перебору дільників."""
    if num < 2:
        return False
    for i in range(2, int(math.isqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime(min_val=100, max_val=1000):
    """Генерує випадкове просте число у заданому діапазоні."""
    prime = random.randint(min_val, max_val)
    while not is_prime(prime):
        prime = random.randint(min_val, max_val)
    return prime

def extended_gcd(a, b):
    """Розширений алгоритм Евкліда."""
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

def mod_inverse(e, phi):
    """Обчислення мультиплікативного оберненого елемента за модулем."""
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Оберненого елемента не існує (числа не взаємно прості).")
    return x % phi

def generate_keypair(min_val=1000, max_val=5000, verbose=False):
    """Генерація пари ключів RSA з можливістю покрокового виводу (verbose)."""
    p = generate_prime(min_val, max_val)
    q = generate_prime(min_val, max_val)
    while p == q:
        q = generate_prime(min_val, max_val)
        
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(2, phi)
    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(2, phi)
        g = math.gcd(e, phi)
        
    d = mod_inverse(e, phi)
    
    if verbose:
        print("\n[~] ДЕТАЛІЗАЦІЯ: Математика генерації ключів (Під капотом)")
        time.sleep(0.5)
        print(f"    [*] 1. Згенеровано великі прості числа: p = {p}, q = {q}")
        time.sleep(0.5)
        print(f"    [*] 2. Обчислено системний модуль: n = p * q = {n}")
        time.sleep(0.5)
        print(f"    [*] 3. Обчислено функцію Ейлера: phi(n) = (p-1)*(q-1) = {phi}")
        time.sleep(0.5)
        print(f"    [*] 4. Вибрано відкриту експоненту e (взаємно просту з phi): {e}")
        time.sleep(0.5)
        print(f"    [*] 5. Обчислено секретну експоненту d: {d}")
        print(f"           (Перевірка Безу: ({e} * {d}) mod {phi} = {(e * d) % phi})")
        time.sleep(1)

    return ((e, n), (d, n))

def hash_message(message):
    """Гешування повідомлення алгоритмом SHA-256 у числове значення."""
    sha_signature = hashlib.sha256(message.encode('utf-8')).hexdigest()
    return int(sha_signature, 16)

def sign_message(message, private_key, verbose=False):
    """Створення ЕЦП з відображенням внутрішніх операцій."""
    d, n = private_key
    
    if verbose:
        print("\n[~] ДЕТАЛІЗАЦІЯ: Процес підписання")
        time.sleep(0.5)
        
    h = hash_message(message)
    if verbose:
        print(f"    [*] 1. Оригінальний геш H(m): {str(h)[:15]}... (скорочено)")
        time.sleep(0.5)
        
    h_mod = h % n 
    if verbose:
        print(f"    [*] 2. Зведення гешу за модулем n: h_mod = {h_mod}")
        time.sleep(0.5)
        
    signature = pow(h_mod, d, n)
    if verbose:
        print(f"    [*] 3. Обчислення підпису: S = (h_mod ^ d) mod n = {signature}")
        time.sleep(1)
        
    return signature

def verify_signature(message, signature, public_key, verbose=False):
    """Верифікація ЕЦП з розгорнутим виводом математики."""
    e, n = public_key
    
    if verbose:
        print("\n[~] ДЕТАЛІЗАЦІЯ: Процес верифікації")
        time.sleep(0.5)
        
    h = hash_message(message)
    h_mod = h % n
    if verbose:
        print(f"    [*] 1. Очікуваний локальний геш документа (h_mod): {h_mod}")
        time.sleep(0.5)
        
    h_decrypted = pow(signature, e, n)
    if verbose:
        print(f"    [*] 2. Розшифровка підпису відкритим ключем: H' = (S ^ e) mod n = {h_decrypted}")
        time.sleep(0.5)
        print(f"    [*] 3. Порівняння: {h_mod} == {h_decrypted}")
        time.sleep(0.5)
        
    return h_mod == h_decrypted

def run_demo():
    """Інтерактивна демонстрація для головного меню."""
    print("-" * 65)
    print("ЗАПУСК БАЗОВОГО АЛГОРИТМУ RSA (З деталізацією процесів)")
    print("-" * 65)
    
    try:
        # Викликаємо генерацію з увімкненим відображенням кроків
        public_key, private_key = generate_keypair(verbose=True)
        print(f"\n[+] Згенерований Відкритий ключ (e, n): {public_key}")
        print(f"[+] Згенерований Закритий ключ (d, n): {private_key}")
        
        message = input("\nВведіть текстове повідомлення для підписання: ").strip()
        if not message:
            message = "Тестове повідомлення для диплому Карп'яка Павла"
            print(f"[*] Використано повідомлення за замовчуванням: '{message}'")
            
        print("\n" + "="*30 + " ПІДПИСАННЯ " + "="*30)
        signature = sign_message(message, private_key, verbose=True)
        print(f"\n[+] ФІНАЛЬНИЙ ЦИФРОВИЙ ПІДПИС: {signature}")
        
        print("\n" + "="*30 + " ВЕРИФІКАЦІЯ " + "="*29)
        is_valid = verify_signature(message, signature, public_key, verbose=True)
        
        if is_valid:
            print("\n[✓] РЕЗУЛЬТАТ: Верифікація УСПІШНА! Підпис справжній та математично підтверджений.")
        else:
            print("\n[✗] РЕЗУЛЬТАТ: Верифікація ПРОВАЛЕНА! Підпис підроблено або повідомлення змінено.")
            
        print("-" * 65)
        input("\nНатисніть Enter, щоб повернутися до головного меню...")
        
    except Exception as e:
         print(f"\n[!] Сталася помилка у модулі rsa_core: {e}")
