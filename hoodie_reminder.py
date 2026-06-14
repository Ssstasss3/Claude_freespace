import requests
import time
from datetime import datetime, timezone, timedelta

BOT_TOKEN = "8675151623:AAHOnCWb3T873lGjOFm_Wp-EQ5f-Ieopjxw"
CHAT_ID = 736449787
MSK = timezone(timedelta(hours=3))
TARGET_HOUR = 6
TARGET_MINUTE = 0

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(text):
    requests.post(f"{API}/sendMessage", json={"chat_id": CHAT_ID, "text": text})

def check_for_reply(last_update_id):
    resp = requests.get(f"{API}/getUpdates", params={"offset": last_update_id + 1, "timeout": 5})
    data = resp.json()
    if data["ok"] and data["result"]:
        return True, data["result"][-1]["update_id"]
    return False, last_update_id

# Get current last update_id so we only look for NEW replies
resp = requests.get(f"{API}/getUpdates").json()
last_update_id = resp["result"][-1]["update_id"] if resp["ok"] and resp["result"] else 0

# Wait until 6:00 MSK
print("Waiting for 6:00 MSK...")
while True:
    now = datetime.now(MSK)
    target = now.replace(hour=TARGET_HOUR, minute=TARGET_MINUTE, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    wait_seconds = (target - now).total_seconds()
    if wait_seconds <= 0:
        break
    print(f"Sleeping for {wait_seconds:.0f} seconds (until {target})")
    time.sleep(min(wait_seconds, 60))
    now = datetime.now(MSK)
    if now.hour == TARGET_HOUR and now.minute >= TARGET_MINUTE:
        break

# Send first reminder
send_message("Good morning, Стас! Don't forget to take a hoodie with you! 🧥")
print("First reminder sent!")

# Keep spamming every 60 seconds until they reply
attempt = 1
while True:
    replied, last_update_id = check_for_reply(last_update_id)
    if replied:
        send_message("Got it! Have a great day! 😎")
        print("User replied, stopping.")
        break
    time.sleep(60)
    attempt += 1
    send_message(f"Hey! Hoodie! Don't forget it! 🧥 (reminder #{attempt})")
    print(f"Reminder #{attempt} sent")
