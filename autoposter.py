import requests
import sqlite3
import time

def send_message(channel_id, message):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    headers = {
        'Authorization': TOKEN,  # Authorization header with the token
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
        print(f"Ошибка отправки сообщения: {response.status_code}")  # Error sending message
        return None

# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('settings.db')  # Connect to the database
    return conn

# Function to create the settings table if it doesn't exist
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

# Function to save settings to the database
def save_settings(conn, token, channel_ids, times, interval, message):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO settings (token, channel_ids, times, interval, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (token, channel_ids, times, interval, message))
    conn.commit()

# Function to get the last saved settings from the database
def get_last_settings(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings ORDER BY id DESC LIMIT 1')
    return cursor.fetchone()

# Create a connection to the database and create the table
conn = create_connection()
create_table(conn)

# Check if there are previous settings to restore
last_settings = get_last_settings(conn)
if last_settings:
    restore = input("Восстановить предыдущую сессию? (да/нет): ").strip().lower()  # Restore previous session? (yes/no)
    if restore == 'да':  # If yes
        TOKEN = last_settings[1]  # Restore token
        CHANNEL_IDS = list(map(int, last_settings[2].split(',')))  # Restore channel IDs
        TIMES = last_settings[3]  # Restore times
        INTERVAL = last_settings[4]  # Restore interval
        MESSAGE = last_settings[5]  # Restore message
    else:  # If no
        TOKEN = input("1. Токен вашего аккаунта: ")  # Your account token
        
        CHANNEL_IDS = list(map(int, input("2. Айди каналов для автопостера (через пробел): ").split()))  # Channel IDs for the auto-poster
        TIMES = input("3. Сколько раз должно отправить?(если бесконечно - inf): ")  # How many times to send? (if infinite - inf)
        INTERVAL = int(input("4. Введите интервал между сообщениями(ввод 1 т.е интервал - 1 секунда): "))  # Enter interval between messages (input 1 for 1 second)
        MESSAGE = input("5. Введите сообщение для авто-постера: ")  # Enter message for the auto-poster
else:  # If no previous settings
    TOKEN = input("1. Токен вашего аккаунта: ")  # Your account token
    
    CHANNEL_IDS = list(map(int, input("2. Айди каналов для автопостера (через пробел): ").split()))  # Channel IDs for the auto-poster
    TIMES = input("3. Сколько раз должно отправить?(если бесконечно - inf): ")  # How many times to send? (if infinite - inf)
    INTERVAL = int(input("4. Введите интервал между сообщениями(ввод 1 т.е интервал - 1 секунда): "))  # Enter interval between messages (input 1 for 1 second)
    MESSAGE = input("5. Введите сообщение для авто-постера: ")  # Enter message for the auto-poster

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
