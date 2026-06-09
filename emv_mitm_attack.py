# emv_mitm_attack.py
import time

class Terminal:
    def __init__(self):
        # Сума транзакції (наприклад, купівля дорогого товару)
        self.amount = 25000 
        self.merchant = "Магазин Електроніки"
        
        # TTQ (Terminal Transaction Qualifiers) - байти налаштувань термінала.
        # Байт 2, Біт 8 (у двійковому вигляді) = 1 означає: "Вимагається перевірка власника (CDCVM / FaceID)"
        self.ttq_normal = "00100000 10000000 00000000 00000000"

    def send_request(self):
        print(f"\n[Термінал] Ініціалізація транзакції: {self.amount} грн ({self.merchant})")
        print(f"[Термінал] Відправка параметрів TTQ: {self.ttq_normal}")
        return {
            "amount": self.amount, 
            "ttq": self.ttq_normal, 
            "merchant": self.merchant
        }

class MitMAttacker:
    def intercept_and_modify(self, terminal_data):
        print("\n[!] Хакер (MitM) перехопив дані між терміналом і смартфоном!")
        time.sleep(1.5)
        
        modified_data = terminal_data.copy()
        
        # Атака Downgrade (зниження рівня безпеки): 
        # Хакер змінює біт вимоги FaceID з 1 на 0 і змінює тип мерчанта на "Транзит" (Метро).
        # У транспортних терміналах FaceID не вимагається для пришвидшення проходу.
        modified_data["ttq"] = "00100000 00000000 00000000 00000000"
        modified_data["merchant"] = "Метрополітен (Підмінено)"
        
        print("[!] Хакер модифікував байти TTQ: Вимкнено вимогу перевірки FaceID/PIN!")
        print(f"[!] Підроблений TTQ, що летить до смартфона: {modified_data['ttq']}")
        time.sleep(1.5)
        return modified_data

class ApplePayDevice:
    def process_transaction(self, data):
        print(f"\n[Смартфон] Отримано запит на оплату від: {data['merchant']}")
        time.sleep(1)
        
        # Смартфон аналізує перехоплений і змінений байт налаштувань (Байт 2)
        ttq_byte_2 = data["ttq"].split()[1]
        
        if ttq_byte_2[0] == '1':
            print("[Смартфон] Аналіз TTQ: Вимагається автентифікація.")
            print("[Смартфон] Очікування FaceID... [УСПІХ]")
            cdcvm_performed = True
        else:
            print("[Смартфон] Аналіз TTQ: Транзитна транзакція (швидкий прохід).")
            print("[Смартфон] КРИТИЧНО: FaceID пропущено згідно з налаштуваннями термінала!")
            cdcvm_performed = False
            
        time.sleep(1)
        print("[Смартфон] Зняття коштів та генерація криптограми ARQC (підпису транзакції)...")
        # ARQC (Authorization Request Cryptogram) генерується на основі суми та дати, 
        # але в класичному EMV він НЕ підписує байти налаштувань TTQ! (У цьому і полягає вразливість)
        arqc = "ARQC_8F3A2B99_VALID"
        
        return {"arqc": arqc, "cdcvm_performed": cdcvm_performed}

def run_demo():
    """
    Інтерактивна демонстрація логічної атаки Man-in-the-Middle (MitM) на EMV протокол.
    """
    print("\n" + "="*65)
    print("  МОДУЛЬ 3: ЛОГІЧНА MitM-АТАКА НА ПРОТОКОЛ EMV (Apple Pay / Visa)")
    print("="*65)
    
    try:
        terminal = Terminal()
        hacker = MitMAttacker()
        iphone = ApplePayDevice()
        
        # 1. Термінал створює легітимний запит
        original_data = terminal.send_request()
        
        # 2. Хакер перехоплює та змінює запит (відбувається атака)
        hacked_data = hacker.intercept_and_modify(original_data)
        
        # 3. Смартфон жертви отримує вже зламані дані
        response = iphone.process_transaction(hacked_data)
        
        print("\n--- РЕЗУЛЬТАТИ ТРАНЗАКЦІЇ ---")
        print(f"[-] Згенерований криптографічний підпис банку (ARQC): {response['arqc']}")
        
        if not response['cdcvm_performed']:
            print("\n[+] УСПІШНА ШАХРАЙСЬКА ТРАНЗАКЦІЯ!")
            print(f"[+] Хакер зняв {terminal.amount} грн з чужого заблокованого телефону у своїй кишені,")
            print("[+] обійшовши біометрію (FaceID) через логічну вразливість протоколу!")
        else:
            print("\n[-] Транзакція захищена. Біометрію було запитано.")
            
    except Exception as e:
         print(f"\n[!] Сталася помилка у модулі emv_mitm_attack: {e}")
         
    print("="*65)
    input("\nНатисніть Enter, щоб повернутися до головного меню...")

if __name__ == "__main__":
    run_demo()