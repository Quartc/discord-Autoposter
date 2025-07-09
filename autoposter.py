import requests
import sqlite3
import time


def send_message(channel_id, message):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        'content': message,
        'allowed_mentions': {
            'parse': ['everyone']
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"Ошибка отправки сообщения: {response.status_code}")
        return None
    

def create_connection():
    conn = sqlite3.connect('settings.db')
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            token TEXT,
            channel_ids TEXT,
            times TEXT,
            interval INTEGER,
            message TEXT
        )
    ''')
    conn.commit()

def save_settings(conn, token, channel_ids, times, interval, message):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO settings (token, channel_ids, times, interval, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (token, channel_ids, times, interval, message))
    conn.commit()

def get_last_settings(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings ORDER BY id DESC LIMIT 1')
    return cursor.fetchone()

conn = create_connection()
create_table(conn)

last_settings = get_last_settings(conn)
if last_settings:
    restore = input("Восстановить предыдущую сессию? (да/нет): ").strip().lower()
    if restore == 'да':
        TOKEN = last_settings[1]
        CHANNEL_IDS = list(map(int, last_settings[2].split(',')))
        TIMES = last_settings[3]
        INTERVAL = last_settings[4]
        MESSAGE = last_settings[5]
    else:
        TOKEN = input("1. Токен вашего аккаунта: ")
        
        CHANNEL_IDS = list(map(int, input("2. Айди каналов для автопостера (через пробел): ").split()))
        TIMES = input("3. Сколько раз должно отправить?(если бесконечно - inf): ")
        INTERVAL = int(input("4. Введите интервал между сообщениями(ввод 1 т.е интервал - 1 секунда): "))
        MESSAGE = input("5. Введите сообщение для авто-постера: ")
else:
    TOKEN = input("1. Токен вашего аккаунта: ")
    
    CHANNEL_IDS = list(map(int, input("2. Айди каналов для автопостера (через пробел): ").split()))
    TIMES = input("3. Сколько раз должно отправить?(если бесконечно - inf): ")
    INTERVAL = int(input("4. Введите интервал между сообщениями(ввод 1 т.е интервал - 1 секунда): "))
    MESSAGE = input("5. Введите сообщение для авто-постера: ")

save_settings(conn, TOKEN, ','.join(map(str, CHANNEL_IDS)), TIMES, INTERVAL, MESSAGE)

x = 0
if TIMES != "inf":
    while x != int(TIMES):
        for CHANNEL_ID in CHANNEL_IDS:
            send_message(CHANNEL_ID, f"{MESSAGE}")
        time.sleep(INTERVAL)
        x += 1
elif TIMES == "inf":
    while True:
        for CHANNEL_ID in CHANNEL_IDS:
            send_message(CHANNEL_ID, f"{MESSAGE}")
        time.sleep(INTERVAL)

conn.close()