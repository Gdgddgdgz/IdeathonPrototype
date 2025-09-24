import json

def upload_tender(name, required_docs, description_keywords=[]):
    """
    Adds a tender to tenders.json
    """
    tender = {
        "name": name,
        "required_docs": required_docs,
        "description_keywords": description_keywords
    }

    try:
        with open("data/tenders.json") as f:
            tenders = json.load(f)
    except FileNotFoundError:
        tenders = []

    tenders.append(tender)
    with open("data/tenders.json", "w") as f:
        json.dump(tenders, f, indent=4)
    return "Tender uploaded successfully!"

