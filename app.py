import os
import re
import requests
from collections import Counter

LOG_FILE = os.environ.get("LOG_FILE_PATH", "auth.log")
THRESHOLD = int(os.environ.get("BRUTEFORCE_THRESHOLD", "3"))
TG_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID", "")

def send_telegram_alert(message):
    if not TG_TOKEN or not TG_CHAT_ID:
        print("[WARN] Токен или Chat ID не заданы. Уведомление в Telegram пропущено.")
        return

    url = f"https://api.telegram.org/{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print(f"[OK] Ответ сервера Telegram: {response.text}")
    except requests.RequestException as error:
        print(f"[ERROR] Ошибка отправки в Telegram: {error}")

def analyze_ssh_logs(file_path, threshold):
    if not os.path.exists(file_path):
        print(f"Файл логов {file_path} не найден.")
        return

    failed_pattern = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)")
    attacker_ips = Counter()

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = failed_pattern.search(line)
            if match:
                ip = match.group(1)
                attacker_ips[ip] += 1

    print("--- Отчет системы обнаружения вторжений (SSH) ---")
    for ip, count in attacker_ips.items():
        if count >= threshold:
            alert_text = f"🚨 [ALERT] Обнаружен брутфорс SSH!\nIP атакующего: {ip}\nНеудачных попыток: {count}"
            print(alert_text)
            send_telegram_alert(alert_text)
        else:
            print(f"[INFO] Подозрительная активность с IP: {ip} (Попыток: {count})")



if __name__ == "__main__":
    analyze_ssh_logs(LOG_FILE, THRESHOLD)
