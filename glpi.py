import os
import requests
import unicodedata
from dotenv import load_dotenv

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL")
APP_TOKEN = os.getenv("APP_TOKEN")
USER_TOKEN = os.getenv("USER_TOKEN")

def normalizar_texto(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = "".join(caractere for caractere in texto if unicodedata.category(caractere) != 'Mn')
    return texto

def iniciar_sessao():
    headers = {
        "Authorization": f"user_token {USER_TOKEN}",
        "App-Token": APP_TOKEN
    }

    response = requests.get(
        f"{GLPI_URL}/initSession",
        headers=headers,
        verify=False
    )

    response.raise_for_status()
    return response.json()["session_token"]

def buscar_usuario_por_email(email):
    session_token = iniciar_sessao()

    headers = {
        "Session-Token": session_token,
        "App-Token": APP_TOKEN
    }

    response = requests.get(
        f"{GLPI_URL}/search/User",
        headers=headers,
        params={
            "criteria[0][field]": 5,
            "criteria[0][searchtype]": "contains",
            "criteria[0][value]": email
        },
        verify=False
    )

    response.raise_for_status()
    return response.json()

def buscar_id_por_nome(endpoint, nome):
    session_token = iniciar_sessao()

    headers = {
        "Session-Token": session_token,
        "App-Token": APP_TOKEN
    }

    response = requests.get(
        f"{GLPI_URL}/{endpoint}",
        headers=headers,
        params={"range": "0-1000"},
        verify=False
    )

    response.raise_for_status()
    itens = response.json()

    nome = nome.lower().strip()

    for item in itens:
        item_nome = str(item.get("name", "")).lower().strip()

        if item_nome == nome:
            return item["id"]

    for item in itens:
        item_nome = str(item.get("name", "")).lower().strip()

        if nome in item_nome:
            return item["id"]

    raise Exception(f"{endpoint} não encontrado: {nome}")

def buscar_id_usuario_por_login_ou_email(valor):
    session_token = iniciar_sessao()

    headers = {
        "Session-Token": session_token,
        "App-Token": APP_TOKEN
    }

    response = requests.get(
        f"{GLPI_URL}/User",
        headers=headers,
        params={"range": "0-1000"},
        verify=False
    )

    response.raise_for_status()
    usuarios = response.json()

    valor_normalizado = normalizar_texto(valor)

    for usuario in usuarios:
        login = normalizar_texto(usuario.get("name", ""))
        email = normalizar_texto(usuario.get("email", ""))
        nome_completo = normalizar_texto(
            f"{usuario.get('firstname', '')} {usuario.get('realname', '')}"
        )

        if valor_normalizado == login:
            return usuario["id"]

        if valor_normalizado == email:
            return usuario["id"]

        if valor_normalizado == nome_completo:
            return usuario["id"]

    raise Exception(f"Usuário não encontrado: {valor}")

def criar_chamado(titulo,
                  descricao,
                  categoria_id,
                  localizacao_id,
                  requerente_id,
                  entidade_id,
                  tipo_id,
                  urgencia_id
                  ):
    
    session_token = iniciar_sessao()

    headers = {
        "Session-Token": session_token,
        "App-Token": APP_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "name": titulo,
            "content": descricao,
            "entities_id": entidade_id,
            "type": tipo_id,
            "urgency": urgencia_id,
            "impact": 3,
            "priority": 3,
            "itilcategories_id": categoria_id,
            "locations_id": localizacao_id,
            "_users_id_requester": requerente_id,
        }
    }

    response = requests.post(
        f"{GLPI_URL}/Ticket",
        headers=headers,
        json=payload,
        verify=False
    )

    response.raise_for_status()
    return response.json()