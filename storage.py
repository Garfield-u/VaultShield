import json
import os

VAULT_FILE = "data/vault.json"


def load_vault():
    if not os.path.exists(VAULT_FILE):
        return []

    with open(VAULT_FILE, "r") as f:
        return json.load(f)


def save_vault(data):
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_entry(entry):
    vault = load_vault()
    vault.append(entry)
    save_vault(vault)


def get_all_entries():
    return load_vault()

def search_entry(keyword):
    vault = load_vault()
    results = []

    for entry in vault:
        if keyword.lower() in entry["label"].lower():
            results.append(entry)

    return results

def delete_entry(keyword):
    vault = load_vault()

    updated_vault = [
        entry for entry in vault
        if keyword.lower() not in entry["label"].lower()
    ]

    save_vault(updated_vault)        