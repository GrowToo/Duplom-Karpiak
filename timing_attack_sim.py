# timing_attack_sim.py
import time
import rsa_core

def vulnerable_sign(message, private_key):
    """Вразлива функція підпису, що використовує Square-and-Multiply."""
    d, n = private_key
    h = rsa_core.hash_message(message) % n
    result = 1
    binary_d = bin(d)[2:]
    timings = []
    
    # Виконується обчислення з імітацією реальних мікрозатримок процесора
    for bit in binary_d:
        start_time = time.perf_counter()
        
        # Square (виконується завжди)
        result = (result * result) % n
        time.sleep(0.01) 
        
        # Multiply (виконується лише для 1)
        if bit == '1':
            result = (result * h) % n
            time.sleep(0.02) 
            
        end_time = time.perf_counter()
        timings.append(end_time - start_time)
        
    return result, timings

def hacker_analyze_timings(timings):
    """Покрокова візуалізація логіки криптоаналітика."""
    print("\n[~] ДЕТАЛІЗАЦІЯ: Аналіз побічного каналу (Timing Analysis)")
    time.sleep(1)
    
    threshold = 0.025
    print(f"    [*] Встановлено порогове значення (Threshold): {threshold} сек")
    print("    [*] Аналізуємо затримки для кожного біта...\n")
    time.sleep(1)
    
    guessed_d_binary = ""
    
    for i, t in enumerate(timings):
        time.sleep(0.2) # Штучна затримка для ефекту покрокового аналізу
        if t >= threshold:
            print(f"    [+] Біт {i:02d} | Час: {t:.4f}s >= {threshold}s -> Було множення! Відновлено біт: '1'")
            guessed_d_binary += "1"
        else:
            print(f"    [-] Біт {i:02d} | Час: {t:.4f}s <  {threshold}s -> Лише квадрат. Відновлено біт: '0'")
            guessed_d_binary += "0"
            
    time.sleep(0.5)
    guessed_d = int(guessed_d_binary, 2)
    return guessed_d, guessed_d_binary

def run_demo():
    print("-" * 65)
    print("МОДУЛЬ 2: АТАКА ПОБІЧНИМИ КАНАЛАМИ (TIMING ATTACK)")
    print("-" * 65)
    
    try:
        print("[*] Генерація цільових ключів RSA (жертви)...")
        # Генерую ключі без детального виводу (verbose=False)
        public_key, private_key = rsa_core.generate_keypair(min_val=100, max_val=500, verbose=False)
        d, n = private_key
        print(f"[+] Справжній секретний ключ (d): {d}")
        print(f"[+] Справжнє бінарне представлення d: {bin(d)[2:]}\n")
        
        message = "Документ високої важливості"
        print(f"[*] Жертва генерує підпис (алгоритм працює...)")
        signature, timings = vulnerable_sign(message, private_key)
        print(f"[+] Підпис згенеровано. Загальний час операції: {sum(timings):.4f} сек.")
        
        # Хакер аналізує час
        guessed_d, guessed_binary = hacker_analyze_timings(timings)
        
        print("\n" + "="*25 + " РЕЗУЛЬТАТИ АТАКИ " + "="*24)
        print(f"[-] Вгаданий хакером бінарний ключ: {guessed_binary}")
        print(f"[-] Вгаданий хакером ключ (d):      {guessed_d}")
        
        if guessed_d == d:
            print("\n[!] КРИТИЧНА ВРАЗЛИВІСТЬ! Хакер ідеально відновив закритий ключ математики RSA,")
            print("    використовуючи виключно аналіз часу виконання мікрооперацій!")
        else:
            print("\n[-] Атака провалилася (можливо, через системні шуми).")
            
    except Exception as e:
         print(f"\n[!] Сталася помилка у модулі timing_attack_sim: {e}")
         
    print("-" * 65)
    input("\nНатисніть Enter, щоб повернутися до головного меню...")
