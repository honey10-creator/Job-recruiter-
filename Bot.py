import os
import requests
from bs4 import BeautifulSoup

# Your direct Telegram credentials
TELEGRAM_BOT_TOKEN = "8746245038:AAFW-TUDab48wZRBVatRSPH_uf1aCPe_UTE"
TELEGRAM_CHAT_ID = "8853414178"

SEEN_FILE = "seen_notifications.txt"


def send_telegram_alert(message):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
  try:
    requests.post(url, json=payload, timeout=10)
  except Exception as e:
    print(f"Error: {e}")


def load_seen():
  if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r") as f:
      return set(line.strip() for line in f)
  return set()


def save_seen(seen_set):
  with open(SEEN_FILE, "w") as f:
    for item in seen_set:
      f.write(f"{item}\n")


def check_govt_jobs():
  target_url = "https://psc.ap.gov.in"
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    response = requests.get(target_url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    seen = load_seen()
    new_found = False

    keywords = [
        "Forest Beat Officer",
        "FBO",
        "Group",
        "SSC",
        "RRB",
        "GDS",
        "Navy",
        "Coast Guard",
        "Notification",
        "Recruitment",
        "Draughtsman",
        "Assistant",
        "Officer",
        "Welfare",
    ]

    for row in soup.find_all("tr"):
      text = " ".join(row.get_text().split())
      if any(key.lower() in text.lower() for key in keywords):
        clean_entry = text[:150]
        if clean_entry not in seen:
          alert_text = (
              f"NEW GOVT JOB NOTIFICATION!\n\nDetails:"
              f" {text[:300]}\n\nCheck Link: {target_url}"
          )
          send_telegram_alert(alert_text)
          seen.add(clean_entry)
          new_found = True

    if new_found:
      save_seen(seen)
      print("New notifications found and sent!")
    else:
      print("No new notifications.")
  except Exception as e:
    print(f"Error checking site: {e}")


if __name__ == "__main__":
  check_govt_jobs()
