import json

def upload_tender(tender_name, required_docs):
    tender = {
        "name": tender_name,
        "required_docs": required_docs
    }

    # Load existing tenders
    try:
        with open("data/tenders.json") as f:
            tenders = json.load(f)
    except FileNotFoundError:
        tenders = []

    tenders.append(tender)
    with open("data/tenders.json", "w") as f:
        json.dump(tenders, f, indent=4)
    return "Tender uploaded successfully!"
