import json
import os

DATA_DIR = "data"
TENDERS_FILE = os.path.join(DATA_DIR, "tenders.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(TENDERS_FILE):
    with open(TENDERS_FILE, "w") as f:
        json.dump([], f)

def upload_tender(name, required_docs, description_keywords):
    with open(TENDERS_FILE, "r") as f:
        tenders = json.load(f)

    new_tender = {
        "name": name,
        "required_docs": required_docs,
        "keywords": description_keywords,
        "submissions": []
    }
    tenders.append(new_tender)

    with open(TENDERS_FILE, "w") as f:
        json.dump(tenders, f, indent=2)

    return f"Tender '{name}' uploaded successfully!"
