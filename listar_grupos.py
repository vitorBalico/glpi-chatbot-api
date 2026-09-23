from glpi import iniciar_sessao, GLPI_URL, APP_TOKEN
import requests

session_token = iniciar_sessao()

headers = {
    "Session-Token": session_token,
    "App-Token": APP_TOKEN
}

response = requests.get(
    f"{GLPI_URL}/Group",
    headers=headers,
    params={"range": "0-1000"},
    verify=False
)

print("Status:", response.status_code)

for grupo in response.json():
    print(grupo.get("id"), "-", grupo.get("name"))