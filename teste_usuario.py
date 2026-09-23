from glpi import iniciar_sessao, GLPI_URL, APP_TOKEN
import requests

session_token = iniciar_sessao()

headers = {
    "Session-Token": session_token,
    "App-Token": APP_TOKEN
}

response = requests.get(
    f"{GLPI_URL}/User",
    headers=headers,
    params={
        "range": "0-1000"
    },
    verify=False
)

print("Status:", response.status_code)

usuarios = response.json()

LOGIN_EXEMPLO = "usuario.exemplo"

for usuario in usuarios:
    login = str(usuario.get("name") or "").strip().casefold()
    if login == LOGIN_EXEMPLO:
        print("Usuario de exemplo encontrado.")
        break
else:
    print("Usuario de exemplo nao encontrado.")
