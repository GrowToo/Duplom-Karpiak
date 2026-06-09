# main.py
import sys
import rsa_core
import timing_attack_sim
import emv_mitm_attack
# Заглушки для майбутніх модулів, які ми розробимо на наступних кроках
# import timing_attack_sim
# import emv_mitm_attack

def print_menu():
    """
    Функція для виведення головного меню програмного стенда.
    Стилізовано для використання в академічних цілях (демонстрація для дипломної роботи).
    """
    print("\n" + "="*65)
    print("      ПРОГРАМНИЙ СТЕНД ДОСЛІДЖЕННЯ СТІЙКОСТІ ЕЦП")
    print("      Розробив: Карп'як Павло")
    print("="*65)
    print("  1. Базова математика RSA (Генерація, підпис, верифікація)")
    print("  2. Атака побічними каналами (Timing Attack) [В розробці]")
    print("  3. Логічна MitM-атака на протокол EMV/Apple Pay [В розробці]")
    print("  4. Вихід з програми")
    print("="*65)

def main():
    """
    Головний цикл програми, який забезпечує безперервну роботу меню
    та перехоплення помилок (try-except).
    """
    while True:
        print_menu()
        try:
            choice = input("Оберіть модуль для запуску (введіть 1, 2, 3 або 4): ").strip()
            
            if choice == '1':
                print("\n[*] Запуск Модуля 1: Базова математика RSA...")
                rsa_core.run_demo()
                
            elif choice == '2':
                print("\n[*] Запуск Модуля 2: Timing Attack...")
                timing_attack_sim.run_demo()
                
            elif choice == '3':
                print("\n[*] Запуск Модуля 3: Логічна MitM-атака...")
                emv_mitm_attack.run_demo()
                
            elif choice == '4':
                print("\n[*] Завершення роботи програмного стенда. До побачення!")
                sys.exit(0)
                
            else:
                print("\n[!] Помилка вводу: Необхідно ввести цифру від 1 до 4.")
                
        except KeyboardInterrupt:
            # Обробка раптового переривання програми (Ctrl+C)
            print("\n\n[*] Роботу програми примусово завершено користувачем.")
            sys.exit(0)
        except Exception as e:
            # Загальне перехоплення будь-яких непередбачуваних помилок
            print(f"\n[!] Виникла критична помилка в роботі стенда: {e}")

if __name__ == "__main__":
    main()