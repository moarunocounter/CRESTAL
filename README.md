# CRESTAL Chat Bot

Bot chat interaktif untuk berkomunikasi dengan agent di platform Nation.fun menggunakan API Crestal Network.

---

## Fitur

- Input Authorization Token, User Address, dan Agent ID secara interaktif
- Kirim pesan manual ke agent
- Kirim pesan otomatis dari file `auto_messages.txt`

---
## SIAPKAN BAHAN INI (Untuk cara dapetinnya ada diTelegram)
1. Agent ID
2. Authorization Token
3. User Address
---

## TUTORIAL MENJALANKAN BOT

1. Masuk ke VPS & Bikin screen
   ```bash
   screen -S crestal
   ```

2. Buat file auto_messages.txt
   ```bash
   nano auto_messages.txt
   ```

3. Clone Repo
    ```bash
    git clone https://github.com/moarunocounter/CRESTAL.git && cd CRESTAL && apt install python3.12-venv -y && python3 -m venv venv-bot && source venv-bot/bin/activate && pip install requests pyfiglet
    ```
    
4. Jalankan bot
   ```bash
   python bot.py
   ```

   



