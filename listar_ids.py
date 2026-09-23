import os
import requests
from dotenv import load_dotenv

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL")
APP_TOKEN = os.getenv("APP_TOKEN")
USER_TOKEN = os.getenv("USER_TOKEN")

headers_login = {
    "Authorization": f"user_token {USER_TOKEN}",
    "App-Token": APP_TOKEN
}

session = requests.get(
    f"{GLPI_URL}/initSession",
    headers=headers_login,
    verify=False
)

session_token = session.json()["session_token"]

headers = {
    "Session-Token": session_token,
    "App-Token": APP_TOKEN
}


def listar(nome, endpoint):
    print (f"\n--- {nome} ---")

    response = requests.get(
        f"{GLPI_URL}/{endpoint}",
        headers=headers,
        params={"range": "0-1000"},
        verify=False
    )

    print("Status:", response.status_code)

    dados = response.json()

    for item in dados:
        nome_item = item.get("completename") or item.get("name")
        print(item.get("id"), "-", nome_item)


listar("CATEGORIAS", "ITILCategory")
listar("LOCALIZACOES", "Location")
listar("USUARIOS", "User")