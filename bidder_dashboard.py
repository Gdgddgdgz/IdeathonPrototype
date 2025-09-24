import json
from utils.probability import calculate_probability
from utils.documents import check_documents

def get_tenders():
    try:
        with open("data/tenders.json") as f:
            return json.load(f)
    except:
        return []

def load_bidder(bidder_id):
    with open("data/bidders.json") as f:
        bidders = json.load(f)
    bidder = next((b for b in bidders if b['id'] == bidder_id), None)
    return bidder

def compare_submission(bidder_id, tender_name, submission_docs, submission_text=""):
    bidder = load_bidder(bidder_id)
    if not bidder:
        return None
    

    tenders = get_tenders()
    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender:
        return None

    probability = calculate_probability(bidder, tender, submission_docs, submission_text)
    present_docs, missing_docs = check_documents(submission_docs, tender)

    return {
        "tender_name": tender_name,
        "probability": probability,
        "present_docs": present_docs,
        "missing_docs": missing_docs
    }

def all_bidders_probabilities(tender_name, submission_text=""):
    """
    Returns a list of dicts: [{'bidder_name':..., 'probability': ...}, ...] for a tender
    """
    with open("data/bidders.json") as f:
        bidders = json.load(f)
    tenders = get_tenders()
    tender = next((t for t in tenders if t['name'] == tender_name), None)
    if not tender:
        return []

    results = []
    for bidder in bidders:
        submission_docs = bidder.get("documents", [])
        prob = calculate_probability(bidder, tender, submission_docs, submission_text)
        results.append({"bidder_name": bidder["name"], "probability": prob})
    return results
