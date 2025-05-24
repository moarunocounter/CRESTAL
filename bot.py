import subprocess
import sys
import time
import os

# ========== UTILITIES WARNA DAN STYLE ==========
class Style:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def print_banner(text):
    import pyfiglet
    banner = pyfiglet.figlet_format(text)
    print(f"{Style.OKGREEN}{banner}{Style.ENDC}")
    print(f"{Style.OKBLUE}{'Telegram @airdropalc'.center(80)}{Style.ENDC}")
    print(f"{Style.OKCYAN}{'='*80}{Style.ENDC}\n")

# ========== CEK DAN INSTALL DEPENDENCY ==========
import shutil

def ensure_pip_installed():
    """Cek dan install pip jika belum tersedia."""
    if shutil.which("pip3") is None:
        print(f"{Style.WARNING}[⚠️] pip belum terinstall. Menginstall pip...{Style.ENDC}")
        try:
            subprocess.check_call(["apt", "update"])
            subprocess.check_call(["apt", "install", "-y", "python3-pip"])
            print(f"{Style.OKGREEN}[✅] pip berhasil diinstall.{Style.ENDC}")
        except Exception as e:
            print(f"{Style.FAIL}[❌] Gagal install pip: {e}{Style.ENDC}")
            sys.exit(1)
    else:
        print(f"{Style.OKGREEN}[✅] pip sudah tersedia.{Style.ENDC}")

def install_and_import(package):
    try:
        __import__(package)
        print(f"{Style.OKGREEN}[✅] Package '{package}' sudah terinstall.{Style.ENDC}")
        return True
    except ImportError:
        print(f"{Style.WARNING}[⚠️] Package '{package}' belum terinstall.{Style.ENDC}")
        return False

def install_package(package):
    print(f"{Style.OKCYAN}[⚙️] Menginstall package '{package}'...{Style.ENDC}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{Style.OKGREEN}[✅] Package '{package}' berhasil diinstall.{Style.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Style.FAIL}[❌] Gagal install package '{package}': {e}{Style.ENDC}")
        sys.exit(1)

def check_dependencies(packages):
    missing = []
    for pkg in packages:
        if not install_and_import(pkg):
            missing.append(pkg)
    return missing

# ========== DAFTAR DEPENDENCIES ==========
required_packages = ["requests", "pyfiglet"]

# Cek pip dulu
ensure_pip_installed()

# Cek dan install paket
missing_packages = check_dependencies(required_packages)

if missing_packages:
    choice = input(f"\n{Style.FAIL}🚨 Package berikut belum terinstall: {missing_packages}{Style.ENDC}\nMau install sekarang? (y/n): ").strip().lower()
    if choice == 'y':
        for pkg in missing_packages:
            install_package(pkg)
        print(f"\n{Style.OKGREEN}[✅] Semua dependencies sudah siap, lanjut jalankan script.{Style.ENDC}\n")
    else:
        print(f"\n{Style.FAIL}[❌] Dependencies belum lengkap. Script tidak bisa berjalan dengan sempurna.{Style.ENDC}\n")
        sys.exit(1)

# ========== SCRIPT UTAMA ==========
import requests
import datetime 

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
                return data[0].get("message", "[No response from agent]")
            elif isinstance(data, dict):
                return data.get("message", "[No response from agent]")
            return "[Response format unexpected]"
        else:
            return f"[❌] Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"[🚨] Exception: {str(e)}"

from datetime import datetime

def format_log(index, total, sender, message):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f"[{timestamp}] [{index}/{total}] {sender}: {message}"

def send_auto_messages(agent_id, user_address, token, filename="auto_messages.txt", delay=2):
    if not os.path.exists(filename):
        print(f"[⚠️] File '{filename}' tidak ditemukan.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    total = len(messages)
    print(f"\n📤 Mengirim {total} auto messages dari '{filename}'...\n")

    for i, msg in enumerate(messages, 1):
        print(format_log(i, total, "🧠 You", msg))
        reply = send_message(msg, agent_id, user_address, token)
        print(format_log(i, total, "🤖 Agent", reply))
        print()
        time.sleep(delay)

# ========== MAIN ==========
print_banner("AIRDROP LEGION")

print(f"{Style.OKCYAN}🤖 Chat with Agent (Nation.fun)\n{Style.ENDC}Masukkan Token, Address EVM, dan Agent ID untuk memulai.\n")

token = input(f"{Style.BOLD}🔑 Authorization Token :{Style.ENDC} ").strip()
user_address = input(f"{Style.BOLD}👤 Address EVM :{Style.ENDC} ").strip()
agent_id_input = input(f"{Style.BOLD}🤖 Agent ID :{Style.ENDC} ").strip()

try:
    agent_id = int(agent_id_input)
except:
    print(f"{Style.WARNING}[⚠️] Agent ID tidak valid, menggunakan default 1821{Style.ENDC}")
    agent_id = 1821

print(f"\n{Style.OKCYAN}Ketik '{Style.BOLD}exit{Style.ENDC}{Style.OKCYAN}' untuk keluar atau '{Style.BOLD}auto{Style.ENDC}{Style.OKCYAN}' untuk kirim auto messages.{Style.ENDC}\n")

while True:
    msg = input(f"{Style.BOLD}🧠 You:{Style.ENDC} ")
    if msg.strip().lower() in ["exit", "quit"]:
        print(f"{Style.FAIL}🚪 Keluar...{Style.ENDC}")
        break
    elif msg.strip().lower() == "auto":
        send_auto_messages(agent_id, user_address, token)
        continue
    reply = send_message(msg, agent_id, user_address, token)
    print(f"{Style.OKBLUE}🤖 Agent: {reply}{Style.ENDC}\n")
