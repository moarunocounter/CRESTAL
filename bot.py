import subprocess
import sys

def install_and_import(package):
    try:
        __import__(package)
        print(f"[✅] Package '{package}' sudah terinstall.")
        return True
    except ImportError:
        print(f"[⚠️] Package '{package}' belum terinstall.")
        return False

def install_package(package):
    print(f"[⚙️] Menginstall package '{package}'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"[✅] Package '{package}' berhasil diinstall.")

def check_dependencies(packages):
    missing = []
    for pkg in packages:
        if not install_and_import(pkg):
            missing.append(pkg)
    return missing

# ===== CEK & INSTALL MODULES DULU =====
required_packages = ["requests", "pyfiglet"]
missing_packages = check_dependencies(required_packages)

if missing_packages:
    choice = input(f"\n🚨 Package berikut belum terinstall: {missing_packages}\nMau install sekarang? (y/n): ").strip().lower()
    if choice == 'y':
        for pkg in missing_packages:
            install_package(pkg)
        print("\n[✅] Semua dependencies sudah siap, lanjut jalankan script.\n")
    else:
        print("\n[❌] Dependencies belum lengkap. Script tidak bisa berjalan dengan sempurna.\n")
        sys.exit(1)

# ================== SCRIPT UTAMA =======================
import requests
import time
import os
import pyfiglet

def print_big_header():
    ascii_art = pyfiglet.figlet_format("AIRDROP LEGION")
    print(ascii_art)
    print("Telegram @airdropalc".center(80))
    print("="*80)
    print()

print_big_header()

url = "https://api.service.crestal.network/v1/chat"

def send_message(msg, agent_id, user_address, token):
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://nation.fun",
        "Authorization": f"Bearer {token}"
    }

    chat_id = f"{user_address}-1744359581"
    payload = {
        "message": msg,
        "agent_id": agent_id,
        "user_address": user_address,
        "chat_id": chat_id
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                reply = data[0].get("message", "[No response from agent]")
            elif isinstance(data, dict):
                reply = data.get("message", "[No response from agent]")
            else:
                reply = "[Response format unexpected]"
            return reply
        else:
            return f"[❌] Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"[🚨] Exception: {str(e)}"

def send_auto_messages(agent_id, user_address, token, filename="auto_messages.txt", delay=2):
    if not os.path.exists(filename):
        print(f"[⚠️] File '{filename}' tidak ditemukan.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    print(f"📤 Mengirim {len(messages)} auto messages dari '{filename}'...\n")
    for msg in messages:
        print(f"🧠 You (auto): {msg}")
        reply = send_message(msg, agent_id, user_address, token)
        print(f"🤖 Agent: {reply}\n")
        time.sleep(delay)  # Delay antar pesan biar gak spam

print("🤖 Chat with Agent (Nation.fun)")
print("Masukkan token Authorization, User Address, dan Agent ID untuk memulai.\n")

token = input("🔑 Authorization Token (Bearer tanpa kata 'Bearer'): ").strip()
user_address = input("👤 User Address (contoh: 0x2D59...): ").strip()
agent_id_input = input("🤖 Agent ID (angka): ").strip()

try:
    agent_id = int(agent_id_input)
except:
    print("[⚠️] Agent ID tidak valid, menggunakan default 1821")
    agent_id = 1821

print("\nKetik 'exit' untuk keluar atau 'auto' untuk kirim auto messages.\n")

while True:
    msg = input("🧠 You: ")
    if msg.strip().lower() in ["exit", "quit"]:
        print("🚪 Keluar...")
        break
    elif msg.strip().lower() == "auto":
        send_auto_messages(agent_id, user_address, token)
        continue
    reply = send_message(msg, agent_id, user_address, token)
    print(f"🤖 Agent: {reply}\n")
