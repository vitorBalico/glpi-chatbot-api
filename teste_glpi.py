import os
import requests
from dotenv import load_dotenv

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL")
APP_TOKEN = os.getenv("APP_TOKEN")
USER_TOKEN = os.getenv("USER_TOKEN")

headers = {
    "Authorization": f"user_token {USER_TOKEN}",
    "App-Token": APP_TOKEN
}

response = requests.get(
    f"{GLPI_URL}/initSession",
    headers=headers,
    verify=False
)

print("Status:", response.status_code)
