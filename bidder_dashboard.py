import json
import os
import random

DATA_DIR = "data"
TENDERS_FILE = os.path.join(DATA_DIR, "tenders.json")
BIDDERS_FILE = os.path.join(DATA_DIR, "bidders.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
for file in [TENDERS_FILE, BIDDERS_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

def get_tenders():
    with open(TENDERS_FILE, "r") as f:
        return json.load(f)

def compare_submission(bidder_id, tender_name, submission_docs, submission_text):
    with open(TENDERS_FILE, "r") as f:
        tenders = json.load(f)
    with open(BIDDERS_FILE, "r") as f:
        bidders = json.load(f)

    tender = next((t for t in tenders if t['name'] == tender_name), None)
    bidder = next((b for b in bidders if b['id'] == bidder_id), None)

    if not tender or not bidder:
        return {"probability": 0, "missing_docs": [], "present_docs": [], "suggestions": []}

    required = tender.get("required_docs", [])
    keywords = tender.get("keywords", [])  # ✅ safe access
    present_docs = [d for d in submission_docs if d in required]
    missing_docs = [d for d in required if d not in submission_docs]

    base_prob = 50
    prob = base_prob + len(present_docs) * 10 - len(missing_docs) * 15
    if any(k.lower() in submission_text.lower() for k in keywords):
        prob += 20
    prob = max(0, min(100, prob))

    # ✅ Suggestions
    suggestions = []
    if missing_docs:
        suggestions.append(f"Add missing documents: {', '.join(missing_docs)}")
    if not any(k.lower() in submission_text.lower() for k in keywords):
        suggestions.append("Include tender-specific keywords in your proposal")
    if prob < 60:
        suggestions.append("Strengthen proposal with more project details or past experience")
    if prob < 40:
        suggestions.append("Reconsider aligning your services with tender requirements")

    return {
        "probability": prob,
        "present_docs": present_docs,
        "missing_docs": missing_docs,
        "suggestions": suggestions
    }

def all_bidders_probabilities(tender_name):
    with open(TENDERS_FILE, "r") as f:
        tenders = json.load(f)
    with open(BIDDERS_FILE, "r") as f:
        bidders = json.load(f)

    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender:
        return []

    results = []
    for bidder in bidders:
        random_prob = random.randint(30, 90)
        results.append({
            "bidder_id": bidder['id'],
            "bidder_name": bidder['name'],
            "probability": random_prob
        })
    return results

def submit_proposal(bidder_id, tender_name, submission_docs, submission_text):
    with open(TENDERS_FILE, "r") as f:
        tenders = json.load(f)

    for tender in tenders:
        if tender['name'] == tender_name:
            if "submissions" not in tender:
                tender["submissions"] = []
            tender['submissions'].append({
                "bidder_id": bidder_id,
                "documents": submission_docs,
                "text": submission_text
            })

    with open(TENDERS_FILE, "w") as f:
        json.dump(tenders, f, indent=2)



