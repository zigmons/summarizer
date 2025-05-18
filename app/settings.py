# app/settings.py
import json
import os

# Onde vamos guardar a chave no disco
_CONFIG_PATH = os.path.expanduser("~/.summarizer_config.json")
VERSION = "0.1.1"

def get_api_key() -> str | None:
    """Lê do arquivo de config; retorna None se não existir."""
    if not os.path.isfile(_CONFIG_PATH):
        return None
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("api_key")

def save_api_key(api_key: str) -> None:
    """Salva (ou sobrescreve) a chave de API em disco."""
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"api_key": api_key}, f)
