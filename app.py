import os
import re
from collections import Counter

# Берем путь к логу и порог срабатывания из переменных окружения (правило DevSecOps)
LOG_FILE = os.environ.get("LOG_FILE_PATH", "auth.log")
THRESHOLD = int(os.environ.get("BRUTEFORCE_THRESHOLD", "3"))

def analyze_ssh_logs(file_path, threshold):
    if not os.path.exists(file_path):
        print(f"Файл логов {file_path} не найден.")
        return

    # Регулярное выражение для поиска IP при неудачном входе по SSH
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
            print(f"[ALERT] Обнаружен брутфорс с IP: {ip} (Неудачных попыток: {count})")
        else:
            print(f"[INFO] Подозрительная активность с IP: {ip} (Попыток: {count})")

if __name__ == "__main__":
    analyze_ssh_logs(LOG_FILE, THRESHOLD)
