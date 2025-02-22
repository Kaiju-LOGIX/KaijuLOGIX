import json
import os

def load_config(config_file="config.json"):
    """
    Lädt die Konfiguration aus der JSON-Datei.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' nicht gefunden.")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

if __name__ == "__main__":
    cfg = load_config()
    print("Konfiguration geladen:")
    print(cfg)

