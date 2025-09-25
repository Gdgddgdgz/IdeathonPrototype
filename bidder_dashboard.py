import json
import os
import random

DATA_DIR = "data"
TENDERS_FILE = os.path.join(DATA_DIR, "tenders.json")
BIDDERS_FILE = os.path.join(DATA_DIR, "bidders.json")

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
for file in [TENDERS_FILE, BIDDERS_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

# ------------------ Tender & Proposal Functions ------------------

def get_tenders():
    with open(TENDERS_FILE, "r") as f:
        return json.load(f)

def save_tenders(tenders):
    with open(TENDERS_FILE, "w") as f:
        json.dump(tenders, f, indent=2)

def compare_submission(bidder_id, tender_name, submission_docs, submission_text):
    tenders = get_tenders()
    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender:
        return None

    required_docs = tender.get("required_docs", [])
    keywords = tender.get("keywords", [])

    present_docs = [d for d in submission_docs if d in required_docs]
    missing_docs = [d for d in required_docs if d not in submission_docs]

    # base probability from documents
    prob = 50 + len(present_docs)*10 - len(missing_docs)*15
    if any(k.lower() in submission_text.lower() for k in keywords):
        prob += 20
    prob = max(0, min(100, prob))

    # Suggestions for bidder improvement
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
    tenders = get_tenders()
    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender or "submissions" not in tender:
        return []

    results = []
    for sub in tender.get("submissions", []):
        docs = sub.get("documents", [])
        text = sub.get("text", "")
        result = compare_submission(sub["bidder_id"], tender_name, docs, text)
        if result:
            results.append({
                "bidder_id": sub["bidder_id"],
                "bidder_name": sub["bidder_id"],
                "probability": result["probability"]
            })
    return results

def submit_proposal(bidder_id, tender_name, documents, text):
    tenders = get_tenders()
    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender:
        return

    if "submissions" not in tender:
        tender["submissions"] = []

    tender["submissions"].append({
        "bidder_id": bidder_id,
        "documents": documents,
        "text": text,
        "rating": None,
        "review": ""
    })

    save_tenders(tenders)

# ------------------ Review & Rating Functions ------------------

def add_review(tender_name, bidder_id, rating, review):
    tenders = get_tenders()
    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender:
        return

    if "submissions" not in tender:
        tender["submissions"] = []

    found = False
    for sub in tender["submissions"]:
        if str(sub["bidder_id"]) == str(bidder_id):
            sub["rating"] = rating
            sub["review"] = review
            found = True
            break

    if not found:
        tender["submissions"].append({
            "bidder_id": bidder_id,
            "documents": [],
            "text": "",
            "rating": rating,
            "review": review
        })

    save_tenders(tenders)

def get_reviews(tender_name):
    tenders = get_tenders()
    tender = next((t for t in tenders if t["name"] == tender_name), None)
    if not tender or "submissions" not in tender:
        return []

    return [
        {"bidder_id": sub.get("bidder_id"), "rating": sub.get("rating"), "review": sub.get("review")}
        for sub in tender["submissions"] if sub.get("review")
    ]
