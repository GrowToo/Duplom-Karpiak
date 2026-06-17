# emv_mitm_attack.py
import time

class Terminal:
    def __init__(self):
        self.amount = 25000 
        self.merchant = "Магазин Електроніки"
        # TTQ (Terminal Transaction Qualifiers)
        self.ttq_normal = "00100000 10000000 00000000 00000000"

    def send_request(self):
        print(f"\n[Термінал] Ініціалізація транзакції: {self.amount} грн ({self.merchant})")
        time.sleep(1)
        print(f"[Термінал] Відправка APDU-пакета з TTQ: {self.ttq_normal}")
        return {"amount": self.amount, "ttq": self.ttq_normal, "merchant": self.merchant}

class MitMAttacker:
    def intercept_and_modify(self, terminal_data):
        print("\n[!] Спрацювало обладнання хакера: Перехоплено радіоканал NFC!")
        time.sleep(1)
        
        print("\n[~] ДЕТАЛІЗАЦІЯ: Логічна атака Downgrade (Зниження безпеки)")
        time.sleep(1)
        print(f"    [*] 1. Оригінальний пакет (TTQ): {terminal_data['ttq']}")
        print("           ^ Другий байт '10000000' вимагає від смартфона перевірку FaceID")
        time.sleep(2)
        
        print("    [*] 2. Втручання в пакет: Застосування XOR-маски для скидання 8-го біта...")
        modified_data = terminal_data.copy()
        modified_data["ttq"] = "00100000 00000000 00000000 00000000"
        modified_data["merchant"] = "Метрополітен (Транзитна зона)"
        time.sleep(1.5)
        
        print(f"    [*] 3. Модифікований пакет (TTQ): {modified_data['ttq']}")
        print("           ^ Другий байт '00000000' (Вимогу FaceID ВИДАЛЕНО)")
        time.sleep(1)
        
        print("[!] Хакер ретранслює зламаний пакет на смартфон жертви...")
        return modified_data

class ApplePayDevice:
    def process_transaction(self, data):
        time.sleep(1.5)
        print(f"\n[Смартфон] Отримано запит на оплату від: {data['merchant']}")
        time.sleep(1)
        
        ttq_byte_2 = data["ttq"].split()[1]
        
        if ttq_byte_2[0] == '1':
            print("[Смартфон] Аналіз TTQ: Вимагається строга автентифікація.")
            print("[Смартфон] Очікування FaceID... [УСПІХ]")
            cdcvm_performed = True
        else:
            print("[Смартфон] Аналіз TTQ: Вимоги перевірки відсутні (Express Transit Mode).")
            print("[Смартфон] КРИТИЧНО: FaceID пропущено! Транзакцію дозволено автоматично.")
            cdcvm_performed = False
            
        time.sleep(1)
        print("[Смартфон] Генерація криптограми ARQC та підпис транзакції...")
        arqc = "ARQC_8F3A2B99_VALID"
        return {"arqc": arqc, "cdcvm_performed": cdcvm_performed}

def run_demo():
    print("-" * 65)
    print("МОДУЛЬ 3: ЛОГІЧНА MitM-АТАКА НА ПРОТОКОЛ EMV (Apple Pay)")
    print("-" * 65)
    
    try:
        terminal = Terminal()
        hacker = MitMAttacker()
        iphone = ApplePayDevice()
        
        # 1. Термінал створює запит
        original_data = terminal.send_request()
        
        # 2. Хакер перехоплює та змінює
        hacked_data = hacker.intercept_and_modify(original_data)
        
        # 3. Смартфон отримує зламані дані
        response = iphone.process_transaction(hacked_data)
        
        print("\n" + "="*23 + " РЕЗУЛЬТАТИ ТРАНЗАКЦІЇ " + "="*22)
        print(f"[-] Криптографічний підпис банку (ARQC): {response['arqc']} (Валідний)")
        
        if not response['cdcvm_performed']:
            print("\n[!] УСПІШНА ШАХРАЙСЬКА ОПЕРАЦІЯ!")
            print(f"    Хакер успішно списав {terminal.amount} грн із заблокованого телефону,")
            print("    обійшовши шифрування завдяки логічній вразливості стандарту EMV.")
        else:
            print("\n[-] Транзакція захищена. Біометрію було запитано.")
            
    except Exception as e:
         print(f"\n[!] Сталася помилка у модулі emv_mitm_attack: {e}")
         
    print("-" * 65)
    input("\nНатисніть Enter, щоб повернутися до головного меню...")

if __name__ == "__main__":
    run_demo()
