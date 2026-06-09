# timing_attack_sim.py
import time
import rsa_core

def vulnerable_sign(message, private_key):
    """
    Вразлива функція підпису, яка використовує класичний алгоритм
    'Square-and-Multiply' для піднесення до степеня за модулем.
    """
    d, n = private_key
    h = rsa_core.hash_message(message) % n
    
    result = 1
    # Отримуємо бінарне представлення секретного ключа (без префікса '0b')
    binary_d = bin(d)[2:]
    
    # Масив для збереження часу обчислення кожного біта (симуляція осцилографа хакера)
    timings = []
    
    for bit in binary_d:
        start_time = time.perf_counter()
        
        # 1. Операція Square (Квадрат) - виконується ЗАВЖДИ для будь-якого біта
        result = (result * result) % n
        time.sleep(0.01) # Штучна затримка мікропроцесора (10 мс)
        
        # 2. Операція Multiply (Множення) - виконується ЛИШЕ для біта '1'
        if bit == '1':
            result = (result * h) % n
            time.sleep(0.02) # Додаткова затримка для множення (20 мс)
            
        end_time = time.perf_counter()
        # Записуємо, скільки часу пішло на обробку цього конкретного біта
        elapsed = end_time - start_time
        timings.append(elapsed)
        
    return result, timings

def hacker_analyze_timings(timings):
    """
    Логіка хакера: криптоаналіз масиву затримок (Side-Channel Analysis).
    """
    print("\n[!] Хакер підключився до плати і виміряв таймінги процесора.")
    print("[!] Починаємо статистичний аналіз затримок...")
    time.sleep(1)
    
    guessed_d_binary = ""
    
    # Встановлюємо порогове значення часу (Threshold).
    # Якщо час обробки біта > 0.025 сек, значить виконувалось і Square, і Multiply.
    threshold = 0.025 
    
    for t in timings:
        if t >= threshold:
            guessed_d_binary += "1"
        else:
            guessed_d_binary += "0"
            
    # Переводимо перехоплений бінарний рядок назад у десяткове число
    guessed_d = int(guessed_d_binary, 2)
    return guessed_d, guessed_d_binary

def run_demo():
    """
    Інтерактивна демонстрація Timing-атаки для консольного меню.
    """
    print("\n" + "="*60)
    print("  МОДУЛЬ 2: АТАКА ПОБІЧНИМИ КАНАЛАМИ (TIMING ATTACK)")
    print("="*60)
    
    try:
        # 1. Генерація невеликих ключів для наочності
        print("[*] Генерація цільових ключів RSA (жертви)...")
        # Беремо невеликі прості числа, щоб двійковий ключ поміщався на екрані
        public_key, private_key = rsa_core.generate_keypair(min_val=100, max_val=500)
        d, n = private_key
        print(f"[+] Справжній секретний ключ (d): {d}")
        print(f"[+] Бінарне представлення d:      {bin(d)[2:]}\n")
        
        # 2. Жертва підписує повідомлення (із вразливою реалізацією)
        message = "Документ високої важливості"
        print(f"[*] Жертва генерує підпис для документа...")
        signature, timings = vulnerable_sign(message, private_key)
        print(f"[*] Підпис згенеровано. Загальний час: {sum(timings):.4f} сек.")
        
        # 3. Хакер проводить атаку
        guessed_d, guessed_binary = hacker_analyze_timings(timings)
        
        print("\n--- РЕЗУЛЬТАТИ АТАКИ ---")
        print(f"[-] Вгаданий хакером бінарний ключ: {guessed_binary}")
        print(f"[-] Вгаданий хакером ключ (d):      {guessed_d}")
        
        if guessed_d == d:
            print("\n[+] КРИТИЧНА ВРАЗЛИВІСТЬ! Хакер повністю відновив секретний ключ d, вимірявши час!")
        else:
            print("\n[-] Атака провалилася (можливо, через системні шуми).")
            
    except Exception as e:
         print(f"\n[!] Сталася помилка у модулі timing_attack_sim: {e}")
         
    print("="*60)
    input("\nНатисніть Enter, щоб повернутися до головного меню...")